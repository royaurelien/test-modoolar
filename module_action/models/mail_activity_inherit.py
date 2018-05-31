from odoo import models, fields, api, exceptions, _, modules
from odoo.http import request
from odoo.exceptions import UserError
from datetime import datetime

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    archived = fields.Boolean(default=False) # Indique si l'activite est terminee

    @api.multi
    def action_create_calendar_event(self):
        """
        Ajout de la société et/ou contact sur le calendrier
        """
        res = super(MailActivity, self).action_create_calendar_event()

        id_res = self.env['res.partner'].search([('id', '=', self.res_id)])

        if self.res_model == 'res.partner':
            if not id_res.parent_id:
                res['context']['default_company_activity_id'] = self.res_id
            else:
                res['context']['default_company_activity_id'] = id_res.parent_id.id
                res['context']['default_contact_activity_id'] = self.res_id

        return res

    def action_feedback(self, feedback=False):
        """
        :param feedback: feedback entre par l'utilisateur
        :return: une action de retour sur la vue precedente
        """
        self.archived = True

        self.feedback = feedback

        new_enr = self.copy() # Copie de l'activite avant sa suppression

        res = super(MailActivity, self).action_feedback(feedback) # Etait return à la base

        if 'active_model' in self._context and self._context['active_model'] != 'calendar.event':
            form_id = self.env.ref('module_action.mail_activity_form_view_for_tree').id

            return {
                "type": 'ir.actions.act_window',
                "name": 'Activités',
                "res_model": 'mail.activity',
                "view_type": 'form',
                "view_mode": 'form',
                "views": [[form_id, 'form']],
                "views_id": {'ref': form_id},
                "view_id": {'ref': form_id},
                "res_id": new_enr.id,
                "target": 'current',
            }

            # return {'type': 'ir.actions.client', 'tag': 'reload'}

        return res

    def unlink_w_meeting(self):
        """
        Methode appelee en JS, ajout d'une verification du fait que l'enregistrement n'a pas deja ete supprime
        """
        res = ''
        events = self.mapped('calendar_event_id')
        if self.exists():
            res = self.unlink()
        if events.exists():
            events.unlink()
        return res

    @api.multi
    def unlink(self):
        """
        Ajout de la suppression de l'evenement associe puis retour sur la vue precedente
        """
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
        """
        Ouvre la vue pour entrer un feedback, depuis le formulaire de la tree view
        """
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
        """
        :return: une action de retour à la vue précédente
        """
        return self.action_feedback(self.feedback)

    def transfert(self):
        """
        Transfert des donnees de la table action a la table des activites
        """
        actions = self.env['crm_yziact.action'].search([])

        for action in actions:
            values = {}

            if action.company_id or action.contact_id:
                values['activity_category'] = action.category
                values['activity_type_id'] = action.type.id
                values['calendar_event_id'] = action.event_id.id
                values['create_date'] = action.create_date
                values['create_uid'] = action.create_uid
                values['date_deadline'] = action.date_end
                values['display_name'] = action.display_name
                values['icon'] = action.icon
                values['note'] = action.description

                if action.status == 'planned':
                    values['archived'] = False
                elif action.status == 'done':
                    values['archived'] = True

                values['write_uid'] = action.write_uid
                values['write_date'] = action.write_date

                if action.user_id:
                    values['user_id'] = action.user_id.id
                else:
                    values['user_id'] = 1

                values['summary'] = action.name

                if datetime.strptime(action.date_end, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') < datetime.today().strftime('%Y-%m-%d'):
                    values['state'] = 'planned'
                elif datetime.strptime(action.date_end, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') == datetime.today().strftime('%Y-%m-%d'):
                    values['state'] = 'today'
                else:
                    values['state'] = 'overdue'

                if action.contact_id:
                    values['res_name'] = action.contact_id.name
                elif action.company_id:
                    values['res_name'] = action.company_id.name

                values['res_model_id'] = self.env['ir.model'].search([('model', '=', 'res.partner')]).id
                values['res_model'] = 'res.partner'

                if action.contact_id:
                    values['res_id'] = action.contact_id.id
                elif action.company_id:
                    values['res_id'] = action.company_id.id

                self.create(values)

            if action.lead_id:
                values['activity_category'] = action.category
                values['activity_type_id'] = action.type.id
                values['calendar_event_id'] = action.event_id.id
                values['create_date'] = action.create_date
                values['create_uid'] = action.create_uid
                values['date_deadline'] = action.date_end
                values['display_name'] = action.display_name
                values['icon'] = action.icon
                values['note'] = action.description

                if action.status == 'planned':
                    values['archived'] = False
                elif action.status == 'done':
                    values['archived'] = True

                values['write_uid'] = action.write_uid
                values['write_date'] = action.write_date
                if action.user_id:
                    values['user_id'] = action.user_id.id
                else:
                    values['user_id'] = 1
                values['summary'] = action.name

                if datetime.strptime(action.date_end, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') < datetime.today().strftime('%Y-%m-%d'):
                    values['state'] = 'planned'
                elif datetime.strptime(action.date_end, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') == datetime.today().strftime('%Y-%m-%d'):
                    values['state'] = 'today'
                else:
                    values['state'] = 'overdue'

                values['res_name'] = action.lead_id.name
                values['res_model_id'] = self.env['ir.model'].search([('model', '=', 'crm.lead')]).id
                values['res_model'] = 'crm.lead'
                values['res_id'] = action.lead_id.id

                self.create(values)

            if action.sale_id:
                values['activity_category'] = action.category
                values['activity_type_id'] = action.type.id
                values['calendar_event_id'] = action.event_id.id
                values['create_date'] = action.create_date
                values['create_uid'] = action.create_uid
                values['date_deadline'] = action.date_end
                values['display_name'] = action.display_name
                values['icon'] = action.icon
                values['note'] = action.description

                if action.status == 'planned':
                    values['archived'] = False
                elif action.status == 'done':
                    values['archived'] = True

                values['write_uid'] = action.write_uid
                values['write_date'] = action.write_date
                if action.user_id:
                    values['user_id'] = action.user_id.id
                else:
                    values['user_id'] = 1
                values['summary'] = action.name

                if datetime.strptime(action.date_end, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') < datetime.today().strftime('%Y-%m-%d'):
                    values['state'] = 'planned'
                elif datetime.strptime(action.date_end, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') == datetime.today().strftime('%Y-%m-%d'):
                    values['state'] = 'today'
                else:
                    values['state'] = 'overdue'

                values['res_name'] = action.sale_id.name
                values['res_model_id'] = self.env['ir.model'].search([('model', '=', 'sale.order')]).id
                values['res_model'] = 'sale.order'
                values['res_id'] = action.sale_id.id

                self.create(values)

            if not action.company_id and not action.contact_id and not action.sale_id and not action.lead_id and action.event_id:
                values['activity_category'] = action.category
                values['activity_type_id'] = action.type.id
                values['calendar_event_id'] = action.event_id.id
                values['create_date'] = action.create_date
                values['create_uid'] = action.create_uid
                values['date_deadline'] = action.date_end
                values['display_name'] = action.display_name
                values['icon'] = action.icon
                values['note'] = action.description

                if action.status == 'planned':
                    values['archived'] = False
                elif action.status == 'done':
                    values['archived'] = True

                values['write_uid'] = action.write_uid
                values['write_date'] = action.write_date
                if action.user_id:
                    values['user_id'] = action.user_id.id
                else:
                    values['user_id'] = 1
                values['summary'] = action.name

                if datetime.strptime(action.date_end, '%Y-%m-%d %H:%M:%S').strftime(
                        '%Y-%m-%d') < datetime.today().strftime('%Y-%m-%d'):
                    values['state'] = 'planned'
                elif datetime.strptime(action.date_end, '%Y-%m-%d %H:%M:%S').strftime(
                        '%Y-%m-%d') == datetime.today().strftime('%Y-%m-%d'):
                    values['state'] = 'today'
                else:
                    values['state'] = 'overdue'

                values['res_name'] = action.event_id.name
                values['res_model_id'] = self.env['ir.model'].search([('model', '=', 'calendar.event')]).id
                values['res_model'] = 'calendar.event'
                values['res_id'] = action.event_id.id

                self.create(values)


class UsersInherit(models.Model):
    _inherit = 'res.users'

    @api.model
    def activity_user_count(self):
        """
        Ajout du fait qu'on ne compte pas les activites archivees, pour le total en haut de chaque page
        """
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

    activities_count = fields.Integer(compute='_activities_count') # Nombre d'activites total
    activities_count_current = fields.Integer(compute='_activities_count') # Nombre d'activites en cours

    @api.one
    def _activities_count(self):
        """
        Calcul pour le bouton dans les fiches client
        Si le partner est une societe, on compte les resultats des ses contacts egalement
        """
        if self.parent_id:
            sale_order = self.env['sale.order'].search([('partner_id', '=', self.id)]).ids  # Devis/bons de commande
            crm_lead = self.env['crm.lead'].search([('partner_id', '=', self.id)]).ids  # Opportunites

            activities_society = self.env['mail.activity'].search([('res_id', '=', self.id), ('res_model', '=', 'res.partner')])  # Liees à la societe
            activities_order = self.env['mail.activity'].search([('res_id', 'in', sale_order), ('res_model', '=', 'sale.order')])  # Liees aux devis/bons de commande
            activities_lead = self.env['mail.activity'].search([('res_id', 'in', crm_lead), ('res_model', '=', 'crm.lead')])  # Liees aux opportunites

            # Equivalent avec seulement les activites en cours
            activities_society_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', '=', self.id), ('res_model', '=', 'res.partner')])
            activities_order_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', 'in', sale_order), ('res_model', '=', 'sale.order')])
            activities_lead_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', 'in', crm_lead), ('res_model', '=', 'crm.lead')])

            self.activities_count = len(activities_society) + len(activities_order) + len(activities_lead)
            self.activities_count_current = len(activities_society_current)  + len(activities_order_current) + len(activities_lead_current)
        else:
            children = self.env['res.partner'].search([('parent_id', '=', self.id)]).ids # Contacts
            sale_order = self.env['sale.order'].search(['|', ('partner_id', '=', self.id), ('partner_id', 'in', children)]).ids # Devis/bons de commande
            crm_lead = self.env['crm.lead'].search(['|', ('partner_id', '=', self.id), ('partner_id', 'in', children)]).ids # Opportunites

            activities_society = self.env['mail.activity'].search([('res_id', '=', self.id), ('res_model', '=', 'res.partner')]) # Liees à la societe
            activities_children = self.env['mail.activity'].search([('res_id', 'in', children), ('res_model', '=', 'res.partner')]) # Liees aux contacts
            activities_order = self.env['mail.activity'].search([('res_id', 'in', sale_order), ('res_model', '=', 'sale.order')]) # Liees devis/bons de commande
            activities_lead = self.env['mail.activity'].search([('res_id', 'in', crm_lead), ('res_model', '=', 'crm.lead')]) # Liees aux opportunites

            # Equivalent avec seulement les activites en cours
            activities_society_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', '=', self.id), ('res_model', '=', 'res.partner')])
            activities_children_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', 'in', children), ('res_model', '=', 'res.partner')])
            activities_order_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', 'in', sale_order), ('res_model', '=', 'sale.order')])
            activities_lead_current = self.env['mail.activity'].search([('archived', '!=', True), ('res_id', 'in', crm_lead), ('res_model', '=', 'crm.lead')])

            self.activities_count = len(activities_society) + len(activities_children) + len(activities_order) + len(activities_lead)
            self.activities_count_current = len(activities_society_current) + len(activities_children_current) + len(activities_order_current) + len(activities_lead_current)

    @api.multi
    def mail_activity_tree_view_action(self):
        """
        Ouverture de la tree view depuis le bouton des fiches clients
        """
        id_doc = self.id
        form_id = self.env.ref('module_action.mail_activity_form_view_for_tree').id

        if self.parent_id:
            sale_order = self.env['sale.order'].search([('partner_id', '=', self.id)]).ids  # Devis/bons de commande
            crm_lead = self.env['crm.lead'].search([('partner_id', '=', self.id)]).ids  # Opportunites

            activities_society = self.env['mail.activity'].search([('res_id', '=', self.id), ('res_model', '=', 'res.partner')]).ids  # Liees à la societe
            activities_order = self.env['mail.activity'].search([('res_id', 'in', sale_order), ('res_model', '=', 'sale.order')]).ids  # Liees devis/bons de commande
            activities_lead = self.env['mail.activity'].search([('res_id', 'in', crm_lead), ('res_model', '=', 'crm.lead')]).ids  # Liees aux opportunites

            return {
                "type": 'ir.actions.act_window',
                "name": 'Activités',
                "res_model": 'mail.activity',
                "view_type": 'form',
                "view_mode": 'list',
                "views": [[False, 'list'], [form_id, 'form']],
                "context": {
                    'search_default_currently': 1,
                    'search_default_mine': 1,
                },
                "views_id": {'ref': 'mail_activity_tree_view_action'},
                "view_id": {'ref': 'mail_activity_tree_view_action'},
                'domain': ['|', '|', ('id', 'in', activities_society), ('id', 'in', activities_order), ('id', 'in', activities_lead)],
                "target": 'current',
            }
        else:
            children = self.env['res.partner'].search([('parent_id', '=', self.id)]).ids  # Contacts
            sale_order = self.env['sale.order'].search(['|', ('partner_id', '=', self.id), ('partner_id', 'in', children)]).ids  # Devis/bons de commande
            crm_lead = self.env['crm.lead'].search(['|', ('partner_id', '=', self.id), ('partner_id', 'in', children)]).ids  # Opportunites

            activities_society = self.env['mail.activity'].search([('res_id', '=', self.id), ('res_model', '=', 'res.partner')]).ids  # Liees à la societe
            activities_children = self.env['mail.activity'].search([('res_id', 'in', children), ('res_model', '=', 'res.partner')]).ids  # Liees aux contacts
            activities_order = self.env['mail.activity'].search([('res_id', 'in', sale_order), ('res_model', '=', 'sale.order')]).ids  # Liees devis/bons de commande
            activities_lead = self.env['mail.activity'].search([('res_id', 'in', crm_lead), ('res_model', '=', 'crm.lead')]).ids  # Liees aux opportunites

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

    company_activity_id = fields.Many2one('res.partner', string="Société",domain="[('company_type','=','company')]", store=True) # Societe liee
    contact_activity_id = fields.Many2one('res.partner', string="Contact",domain="[('company_type','=','person'), ('parent_id','=',company_activity_id)]", store=True) # Contact lie

    @api.model
    def create(self, values):
        """
        Creation d'une activite si un evenement est cree avec une societe et/ou un contact, ajout d'un participant si la creation vient d'une activite
        """
        if not values.get('activity_ids'):
            defaults = self.default_get(['activity_ids', 'res_model_id', 'res_id', 'user_id'])
            res_model_id = values.get('res_model_id', defaults.get('res_model_id'))
            res_id = values.get('res_id', defaults.get('res_id'))
            if not defaults.get('activity_ids') and not res_model_id and not res_id:
                if values.get('company_activity_id') or values.get('contact_activity_id'):
                    res_model_id = self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1).id

                if values.get('contact_activity_id'):
                    res_id = values.get('contact_activity_id')
                else:
                    res_id = values.get('company_activity_id')
                values['res_id'] = res_id
                values['res_model_id'] = res_model_id

        result = super(CalendarEvent, self).create(values)

        if result.activity_ids:
            if result.activity_ids[0].res_model == 'res.partner':
                participant = self.env['res.partner'].search([('id', '=', result.activity_ids[0].res_id)])
                result.partner_ids = result.partner_ids + participant

        return result

    def end_activity(self):
        """
        Ouvre la vue pour entrer un feedback, depuis le formulaire de la tree view
        """
        activity = self.env['mail.activity'].search([('calendar_event_id', '=', self.id)])

        view_id = self.env.ref('module_action.mail_activity_form_feedback').id

        if activity[0] and activity[0].archived == False:
            return {
                "type": 'ir.actions.act_window',
                "name": 'Activités',
                "res_model": 'mail.activity',
                "view_mode": 'form',
                "view_type": 'form',
                "views": [[view_id, 'form']],
                'res_id': activity[0].id,
                "view_id": view_id,
                "target": 'new',
            }
        else:
            raise UserError(_("L'activité est déjà archivée."))













