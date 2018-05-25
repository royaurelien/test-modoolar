from odoo import models, fields, api, exceptions, _, modules
from odoo.http import request
from odoo.exceptions import UserError

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    archived = fields.Boolean(default=False)

    def action_feedback(self, feedback=False):
        self.archived = True

        self.feedback = feedback

        self.copy()

        res = super(MailActivity, self).action_feedback(feedback) # Etait return à la base

        return {'type': 'ir.actions.client', 'tag': 'history_back'} or res

    def unlink_w_meeting(self):
        res = ''
        events = self.mapped('calendar_event_id')
        if self.exists():
            res = self.unlink()
        if events.exists():
            events.unlink()
        return res

    @api.multi
    def unlink(self):
        self._check_access('unlink')

        for activity in self:
            if activity.date_deadline <= fields.Date.today():
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', activity.user_id.partner_id.id),
                    {'type': 'activity_updated', 'activity_deleted': True})

            if activity.calendar_event_id != False and self.archived != True:
                    activity.calendar_event_id.unlink()

        if self.exists():
            res = super(MailActivity, self.sudo()).unlink()

        return {'type': 'ir.actions.client', 'tag': 'history_back'} or res

    def open_feedback_form(self):
        view_id = self.env.ref('module_action.mail_activity_form_feedback').id
        return {
            "type": 'ir.actions.act_window',
            "name": 'Activités',
            "res_model": 'mail.activity',
            "view_mode": 'form',
            "view_type": 'form',
            "views": [[view_id, 'form']],
            'res_id': self.id,
            "view_id": view_id,
            "target": 'new',
        }

    @api.multi
    def action_done_with_feedback(self):
        return self.action_feedback(self.feedback)


class UsersInherit(models.Model):
    _inherit = 'res.users'

    @api.model
    def activity_user_count(self):
        query = """SELECT m.name, count(*), act.res_model as model,
                            CASE
                                WHEN now()::date - act.date_deadline::date = 0 Then 'today'
                                WHEN now()::date - act.date_deadline::date > 0 Then 'overdue'
                                WHEN now()::date - act.date_deadline::date < 0 Then 'planned'
                            END AS states
                        FROM mail_activity AS act
                        JOIN ir_model AS m ON act.res_model_id = m.id
                        WHERE user_id = %s AND archived IS NOT TRUE
                        GROUP BY m.name, states, act.res_model;
                        """
        self.env.cr.execute(query, [self.env.uid])
        activity_data = self.env.cr.dictfetchall()

        user_activities = {}
        for activity in activity_data:
            if not user_activities.get(activity['model']):
                user_activities[activity['model']] = {
                    'name': activity['name'],
                    'model': activity['model'],
                    'icon': modules.module.get_module_icon(self.env[activity['model']]._original_module),
                    'total_count': 0, 'today_count': 0, 'overdue_count': 0, 'planned_count': 0,
                }
            user_activities[activity['model']]['%s_count' % activity['states']] += activity['count']
            if activity['states'] in ('today', 'overdue'):
                user_activities[activity['model']]['total_count'] += activity['count']

        return list(user_activities.values())

class PartnerInherit(models.Model):
    _inherit = 'res.partner'

    activities_count = fields.Integer(compute='_activities_count')
    activities_count_current = fields.Integer(compute='_activities_count')

    @api.one
    def _activities_count(self):
        children = self.env['res.partner'].search([('parent_id', '=', self.id)]).ids
        sale_order = self.env['sale.order'].search(['|', ('partner_id', '=', self.id), ('partner_id', 'in', children)]).ids
        crm_lead = self.env['crm.lead'].search(['|', ('partner_id', '=', self.id), ('partner_id', 'in', children)]).ids

        activities_society = self.env['mail.activity'].search([('res_id', '=', self.id), ('res_model', '=', 'res.partner')])
        activities_children = self.env['mail.activity'].search([('res_id', 'in', children), ('res_model', '=', 'res.partner')])
        activities_order = self.env['mail.activity'].search([('res_id', 'in', sale_order), ('res_model', '=', 'sale.order')])
        activities_lead = self.env['mail.activity'].search([('res_id', 'in', crm_lead), ('res_model', '=', 'crm.lead')])

        activities_society_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', '=', self.id), ('res_model', '=','res.partner')])
        activities_children_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', 'in', children), ('res_model', '=', 'res.partner')])
        activities_order_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', 'in', sale_order), ('res_model', '=', 'sale.order')])
        activities_lead_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', 'in', crm_lead), ('res_model', '=', 'crm.lead')])

        if self.parent_id:
            self.activities_count = len(activities_society)
            self.activities_count_current = len(activities_society_current)
        else:
            self.activities_count = len(activities_society)+len(activities_children)+len(activities_order)+len(activities_lead)
            self.activities_count_current = len(activities_society_current) + len(activities_children_current) + len(activities_order_current) + len(activities_lead_current)

    @api.multi
    def mail_activity_tree_view_action(self):

        id_doc = self.id

        children = self.env['res.partner'].search([('parent_id', '=', self.id)]).ids
        sale_order = self.env['sale.order'].search(
            ['|', ('partner_id', '=', self.id), ('partner_id', 'in', children)]).ids
        crm_lead = self.env['crm.lead'].search(['|', ('partner_id', '=', self.id), ('partner_id', 'in', children)]).ids

        activities_society = self.env['mail.activity'].search(
            [('res_id', '=', self.id), ('res_model', '=', 'res.partner')]).ids
        activities_children = self.env['mail.activity'].search(
            [('res_id', 'in', children), ('res_model', '=', 'res.partner')]).ids
        activities_order = self.env['mail.activity'].search(
            [('res_id', 'in', sale_order), ('res_model', '=', 'sale.order')]).ids
        activities_lead = self.env['mail.activity'].search([('res_id', 'in', crm_lead), ('res_model', '=', 'crm.lead')]).ids

        form_id = self.env.ref('module_action.mail_activity_form_view_for_tree').id
        return {
            "type": 'ir.actions.act_window',
            "name": 'Activités',
            "res_model": 'mail.activity',
            "view_type": 'form',
            "view_mode": 'list',
            "views": [[False, 'list'],[form_id, 'form']],
            "context": {
                'search_default_currently': 1,
                'search_default_mine': 1,
            },
            "views_id": {'ref': 'mail_activity_tree_view_action'},
            "view_id": {'ref': 'mail_activity_tree_view_action'},
            'domain':['|','|','|',('id', 'in', activities_society), ('id', 'in', activities_children), ('id', 'in', activities_order), ('id', 'in', activities_lead)],
            "target": 'current',
        }

class CalendarEvent(models.Model):
    _inherit = ['calendar.event']

    @api.model
    def create(self, values):
        if not values.get('activity_ids'):
            defaults = self.default_get(['activity_ids', 'res_model_id', 'res_id', 'user_id'])
            res_model_id = values.get('res_model_id', defaults.get('res_model_id'))
            res_id = values.get('res_id', defaults.get('res_id'))
            if not defaults.get('activity_ids') and not res_model_id and not res_id:
                if values.get('company_id') or values.get('contact_id'):
                    res_model_id = self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1).id

                if values.get('contact_id'):
                    res_id = values.get('contact_id')
                else:
                    res_id = values.get('company_id')
                values['res_id'] = res_id
                values['res_model_id'] = res_model_id

        result = super(CalendarEvent, self).create(values)



        return result













