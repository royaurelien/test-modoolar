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

        res = super(MailActivity, self).action_feedback(feedback)  # Etait return à la base

        events = new_enr.mapped('calendar_event_id')
        if feedback:
            for event in events:
                description = event.description
                tab_res = description.split('Feedback')
                description = '<p>%s</p>\n%s%s' % (tab_res[0] or '', _("Feedback: "), feedback)
                event.write({'description': description})

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
        Ne pas utiliser tel quel :
        - dans le calandrier, company_id et contact_id doivent être transférés dans les deux nouveaux champ équivalents
        - Les actions sont automatiquement créées sur les RDV, faire en sorte qu'il n'y ait aucun doublon
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
    activity_archived = fields.Boolean(compute='_compute_activity_button')
    activity_exist = fields.Boolean(compute='_compute_activity_button', default=False)

    @api.multi
    def _compute_activity_button(self):
        for event in self:
            activity = self.env['mail.activity'].search([('summary', '=', event.name),('calendar_event_id', '=', event.id), ('date_deadline', '=', event.start_datetime)], limit=1)
            if activity:
                event.activity_archived = activity.archived
                event.activity_exist = True
            else:
                event.activity_exist = False

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
                values['res_model'] = 'res.partner'
        if values.get('company_activity_id') or values.get('contact_activity_id'):
            if values.get('contact_activity_id'):
                values['res_id'] = values.get('contact_activity_id')
            else:
                values['res_id'] = values.get('company_activity_id')

            values['res_model_id'] = self.env['ir.model'].search([('model', '=', 'res.partner')]).id
            values['res_model'] = 'res.partner'

        result = super(CalendarEvent, self).create(values)

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

    # Deux methodes pour mettre les coordonnees de la societe ou du contact en description, et changer cette derniere en fonction des modifications
    @api.onchange('contact_activity_id')
    def onchange_contact_coordonnees(self):
        country_name = ''

        # Si le contact a change ou a ete ajoute
        if self.contact_activity_id:
            if self.contact_activity_id.country_id:
                country_name = self.env['res.country'].search([('id', '=', self.contact_activity_id.country_id.id)])
                country_name = country_name[0].name

            string_to_add = '%s\n%s - %s\n%s\n%s %s\n%s %s\n%s\n__________\n' % (self.contact_activity_id.name or '',
                                                                                 self.contact_activity_id.phone or '',
                                                                                 self.contact_activity_id.mobile or '',
                                                                                 self.contact_activity_id.email or '',
                                                                                 self.contact_activity_id.street or '',
                                                                                 self.contact_activity_id.street2 or '',
                                                                                 self.contact_activity_id.zip or '',
                                                                                 self.contact_activity_id.city or '',
                                                                                 country_name or '')
            desc = self.description
            if self.description == False:
                desc = ['', '']
            else:
                desc = self.description.split('__________')

            if len(desc) == 1:
                self.description = '%s%s' % (string_to_add, desc[0])
            elif len(desc) > 1:
                self.description = '%s%s' % (string_to_add, desc[1])

        # Si le contact est supprime
        elif not self.contact_activity_id:
            # Suppression si pas de societe
            if not self.company_activity_id:
                string_to_add = ' \n__________\n'
            # Si societe, description de la societe
            elif self.company_activity_id:
                if self.company_activity_id.country_id:
                    country_name = self.env['res.country'].search([('id', '=', self.company_activity_id.country_id.id)])
                    country_name = country_name[0].name

                string_to_add = '%s\n%s - %s\n%s\n%s %s\n%s %s\n%s\n__________\n' % (
                self.company_activity_id.name or '',
                self.company_activity_id.phone or '',
                self.company_activity_id.mobile or '',
                self.company_activity_id.email or '',
                self.company_activity_id.street or '',
                self.company_activity_id.street2 or '',
                self.company_activity_id.zip or '',
                self.company_activity_id.city or '',
                country_name or '')

            desc = self.description
            if self.description == False:
                desc = ['', '']
            else:
                desc = self.description.split('__________')

            if len(desc) == 1:
                self.description = '%s%s' % (string_to_add, desc[0])
            elif len(desc) > 1:
                self.description = '%s%s' % (string_to_add, desc[1])


    @api.onchange('company_activity_id')
    def onchange_company_coordonnees(self):
        self.contact_activity_id = False
        country_name = ''
        # Description de la societe
        if self.company_activity_id:
            if self.company_activity_id.country_id:
                country_name = self.env['res.country'].search([('id', '=', self.company_activity_id.country_id.id)])
                country_name = country_name[0].name

            string_to_add = '%s\n%s - %s\n%s\n%s %s\n%s %s\n%s\n__________\n' % (self.company_activity_id.name or '',
                                                                                 self.company_activity_id.phone or '',
                                                                                 self.company_activity_id.mobile or '',
                                                                                 self.company_activity_id.email or '',
                                                                                 self.company_activity_id.street or '',
                                                                                 self.company_activity_id.street2 or '',
                                                                                 self.company_activity_id.zip or '',
                                                                                 self.company_activity_id.city or '',
                                                                                 country_name or '')
            desc = self.description
            if self.description == False:
                desc = ['', '']
            else:
                desc = self.description.split('__________')

            if len(desc) == 1:
                self.description = '%s%s' % (string_to_add, desc[0])
            elif len(desc) > 1:
                self.description = '%s%s' % (string_to_add, desc[1])
        # Si suppression de la societe, suppression de la description
        elif not self.company_activity_id:
            string_to_add = ' \n__________\n'
            desc = self.description
            if self.description == False:
                desc = ['', '']
            else:
                desc = self.description.split('__________')

            if len(desc) == 1:
                self.description = '%s%s' % (string_to_add, desc[0])
            elif len(desc) > 1:
                self.description = '%s%s' % (string_to_add, desc[1])

    # Lorsqu'un contact ou la societe change, changement de l'activite (supprimer, modifier le partner...)
    @api.multi
    def write(self, values):
        # Si modification sur la societe ou le contact
        if 'company_activity_id' in values or 'contact_activity_id' in values:
            activity = self.env['mail.activity'].search([('res_model', '=', 'res.partner'), ('summary', '=', self.name),('calendar_event_id', '=', self.id), ('archived', '=', False)], limit=1)
            activity_not_partner = self.env['mail.activity'].search([('res_model', '!=', 'res.partner'), ('summary', '=', self.name),('calendar_event_id', '=', self.id), ('archived', '=', False)], limit=1)

            if activity:
                # Ajout ou changement du contact
                if 'contact_activity_id' in values and values.get('contact_activity_id') != False:
                    activity.write({'res_id': values.get('contact_activity_id')})
                    self.res_id = values.get('contact_activity_id')
                    self.res_model = 'res.partner'
                    self.res_model_id = self.env['ir.model'].search([('model', '=', 'res.partner')]).id
                # Suppression du contact
                elif 'contact_activity_id' in values and values.get('contact_activity_id') == False:
                    # Ajout/modification d'une societe
                    if 'company_activity_id' in values and values.get('company_activity_id') != False:
                        activity.write({'res_id': values.get('company_activity_id')})
                        self.res_id = values.get('company_activity_id')
                        self.res_model = 'res.partner'
                        self.res_model_id = self.env['ir.model'].search([('model', '=', 'res.partner')]).id
                    # Suppression de la societe
                    elif 'company_activity_id' in values and values.get('company_activity_id') == False:
                        activity.write({'calendar_event_id': False})
                        activity.unlink()
                        if activity_not_partner:
                            self.res_id = activity_not_partner.res_id
                            self.res_model = activity_not_partner.res_model
                            self.res_model_id = activity_not_partner.res_model_id
                        else:
                            self.res_id = False
                            self.res_model = False
                            self.res_model_id = False
                    # Pas d'ajout/modification ou de suppression de societe, et pas de societe avant
                    elif 'company_activity_id' not in values and not self.company_activity_id:
                        activity.write({'calendar_event_id': False})
                        activity.unlink()
                        if activity_not_partner:
                            self.res_id = activity_not_partner.res_id
                            self.res_model = activity_not_partner.res_model
                            self.res_model_id = activity_not_partner.res_model_id
                        else:
                            self.res_id = False
                            self.res_model = False
                            self.res_model_id = False
                    # Pas d'ajout/modification ou de suppression de societe, et societe deja presente
                    elif 'company_activity_id' not in values and self.company_activity_id:
                        activity.write({'res_id': self.company_activity_id})
                        self.res_id = self.company_activity_id
                        self.res_model = 'res.partner'
                        self.res_model_id = self.env['ir.model'].search([('model', '=', 'res.partner')]).id
                # Pas de contact touche et suppression de la societe
                elif 'contact_activity_id' not in values and 'company_activity_id' in values and values.get('company_activity_id') == False:
                    activity.write({'calendar_event_id': False})
                    activity.unlink()
                    if activity_not_partner:
                        self.res_id = activity_not_partner.res_id
                        self.res_model = activity_not_partner.res_model
                        self.res_model_id = activity_not_partner.res_model_id
                    else:
                        self.res_id = False
                        self.res_model = False
                        self.res_model_id = False
                # Pas de contact touche et ajout/modification de societe
                elif 'contact_activity_id' not in values and 'company_activity_id' in values and values.get('company_activity_id') != False:
                    activity.write({'res_id': values.get('company_activity_id')})
                    self.res_id = values.get('company_activity_id')
                    self.res_model = 'res.partner'
                    self.res_model_id = self.env['ir.model'].search([('model', '=', 'res.partner')]).id
                else:
                    pass
            else:
                # Si pas d'activite auparavant, la creer
                val = {}

                meeting_activity_type = self.env['mail.activity.type'].search([('category', '=', 'meeting')],limit=1)
                model = self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1)[0]

                val['res_model_id'] = model.id
                val['res_model'] = 'res.partner'
                val['activity_type_id'] = meeting_activity_type[0].id

                if 'name' in values:
                    val['summary'] = values.get('name')
                else:
                    val['summary'] = self.name

                if 'description' in values:
                    val['note'] = values.get('description')
                else:
                    val['note'] = self.description

                if 'start_datetime' in values:
                    val['date_deadline'] = values.get('start_datetime')
                else:
                    val['date_deadline'] = self.start_datetime

                if 'user_id' in values:
                    val['user_id'] = values.get('user_id')
                else:
                    val['user_id'] = self.user_id.id

                val['calendar_event_id'] = self.id

                val['archived'] = False


                if 'contact_activity_id' in values:
                    contact = self.env['res.partner'].search([('id', '=', values.get('contact_activity_id'))])[0]
                    val['res_id'] = values.get('contact_activity_id')
                    val['res_name'] = contact.name
                    res = self.env['mail.activity'].create(val)
                    values['res_id'] = values.get('contact_activity_id')
                elif 'company_activity_id' in values:
                    company = self.env['res.partner'].search([('id', '=', values.get('company_activity_id'))])[0]
                    val['res_id'] = values.get('company_activity_id')
                    val['res_name'] = company.name
                    res = self.env['mail.activity'].create(val)
                    values['res_id'] = values.get('company_activity_id')

                values['activity_ids'] = [(6, 0, [res.id])]

                values['res_model'] = 'res.partner'
                values['res_model_id'] = self.env['ir.model'].search([('model', '=', 'res.partner')]).id

        result = super(CalendarEvent, self).write(values)

        return result