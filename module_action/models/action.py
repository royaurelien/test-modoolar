# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta
from operator import itemgetter, attrgetter


class Action(models.Model):
    _name = 'crm_yziact.action'
    _inherit = ['mail.thread']
    _description = "Crm Action"
    _order = "date"

    ######DEFAULT####
    def get_user(self):
        uid = self._context.get('uid', False)
        user_id = self.env['res.users'].browse(uid).id

        return user_id

    def get_datetime(self):
        return datetime.now()


    ######SELECTION####
    status = fields.Selection([
        ('planned',u'Plannifiée'),
        ('running', u'En Cours'),
        ('done', u'Terminée')
    ], string='Statut', default='planned')
    regarding = fields.Selection([
        ('lead', 'Piste/Opp'),
        ('company', 'Compte'),
        ('contact', 'Contact'),
        ('sale', 'Vente')
    ], string='Concernant')

    ######TEXT####
    name = fields.Char(string="Nom", track_visibility="always", required=True)
    description = fields.Text(string='Compte rendu')

    ######DATE####
    # date = fields.Datetime(string='Date', default=datetime.now(), compute='date_debut_trigger', inverse='get_true', store=True, required=True,)
    date = fields.Datetime(string='Date debut', default=get_datetime, required=True)
    #to create an rdv and be capable to modifie the dates of both event and action
    date_debut = fields.Datetime(string='Date debut', compute='get_date', inverse='get_true', store=True, related="event_id.start_datetime")
    date_end = fields.Datetime(string='Date fin', compute='get_date', inverse='get_true', store=True, related="event_id.stop")
    #to make a filter on today i need a date without time
    date_filter = fields.Date(string='Date', compute='get_date', store=True)

    ######BOOLEAN####
    active = fields.Boolean(default=True)

    ######RELATIONEL####
    user_id = fields.Many2one(comodel_name='res.users', string=u'Assigné à')
    type = fields.Many2one(comodel_name='mail.activity.type', track_visibility="always", required=True)
    company_id = fields.Many2one(comodel_name='res.partner', string=u"Société", domain="[('company_type','=','company')]", track_visibility="always")
    contact_id = fields.Many2one(comodel_name='res.partner', string=u"Contact", domain="[('company_type','=','person'), ('parent_id','=',company_id)]")
    sale_id = fields.Many2one(comodel_name='sale.order', string="Vente", domain="['|',('partner_id','=',company_id), ('partner_id','=',contact_id)]", track_visibility="always")
    lead_id = fields.Many2one(comodel_name='crm.lead', string=u"Piste / Opportunité", domain="[('partner_id','=',company_id)]", track_visibility="always")
    event_id = fields.Many2one(comodel_name='calendar.event', string="Rendez-vous", store=True)

    @api.model
    def create(self, vals):
        calendar_env = self.env['calendar.event']
        user_env = self.env['res.users']
        user_obj = user_env.browse(vals.get('user_id', self._uid))
        event = None
        print(vals.get('regarding', False))
        if not vals.get('regarding', False) :
            regard = False

            if vals.get('sale_id', False):
                regard = 'sale'
            elif vals.get('lead_id', False):
                regard = 'lead'
            elif vals.get('contact_id', False):
                regard = 'contact'
            elif vals.get('company_id', False):
                regard = 'company'

            vals['regarding'] = regard

        res = super(Action, self).create(vals)
        date_end = vals.get('date_end',False)
        if not date_end :
            date_end = datetime.strptime(res.date, '%Y-%m-%d %H:%M:%S') + timedelta(hours=1)
            date_end = date_end.strftime('%Y-%m-%d %H:%M:%S')

        if vals.get('type',False) == 3 and not vals.get('event_id', False) :
            event = calendar_env.create({
                'name': res.name,
                'partner_ids': [(6, False,[user_obj.partner_id.id])],
                'start':res.date,
                'stop':date_end,
                'start_datetime': res.date,
                'stop_datetime':date_end,
                'desciption': res.description,
                'action_id':res.id,
            })
            res.event_id = event.id

        if res.company_id:
            res.company_id.change_date_action(res.date)


        return res


    @api.multi
    def unlink(self):
        context = {}

        if self._context:
            context = self._context

        for lead in self:
            if not context.get('event', False):
                if lead.event_id:
                    lead.event_id.with_context(action=True).unlink()
            super(Action, lead).unlink()


    @api.depends('date')
    def get_date(self):
        for action in self:
            action.date_filter = action.date

            if action.date_debut != action.date:
                action.date_debut = action.date

            if not action.date_end or action.date_end < action.date:
                action.date_end = datetime.strptime(action.date, '%Y-%m-%d %H:%M:%S') + timedelta(hours=1)


    def get_true(self):
        return  True



class PartnerActions(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def get_nb_action(self):
        print( "[%s] our res.partner get_nb_action" % __name__)
        action_env = self.env['crm_yziact.action']
        for partner in self:
            action_count = action_env.search([('company_id', '=', partner.id)])
            partner.action_count = len(action_count)

            if action_count:
                action_decroissant = sorted(action_count, key=attrgetter('date'), reverse=True)
                partner.last_action = action_decroissant[0].date

    @api.multi
    def get_contact_nb_action(self):
        print( "[%s] our res.partner get_contact_nb_action" % __name__)
        action_env = self.env['crm_yziact.action']
        for partner in self:
            action_count = action_env.search([('contact_id', '=', partner.id)])
            partner.contact_action_count = len(action_count)

    action_count = fields.Integer('Action', compute=get_nb_action)
    contact_action_count = fields.Integer('Action', compute=get_contact_nb_action)

    last_action = fields.Date(u'Date dernière action')

    @api.multi
    def action_view_action(self):
        if 'person' in self.company_type:
            action = {
                "type": "ir.actions.act_window",
                "name": "Action Commerciales",
                "res_model": "crm_yziact.action",
                "view_type": 'form',
                "views": [[False, "tree"], [False, "form"]],
                "domain":[('contact_id','=', self.id)],
                "context": {
                    'contact_id': self.id,
                    'search_default_contact_id': self.id,
                    'default_company_id': self.parent_id.id,
                    'default_regarding':'contact',
                },
                'views_id': {'ref': "crm_yziact.action_com_tree"},
                "target": 'current',
            }

        else:
            action = {
                "type": "ir.actions.act_window",
                "name": "Action Commerciales",
                "res_model": "crm_yziact.action",
                "view_type": 'form',
                "views": [[False, "tree"], [False, "form"]],
                "domain": [('company_id', '=', self.id)],
                "context": {'company_id': self.id ,
                            'search_default_company_id': self.id,
                            'default_regarding': 'company',
                            },
                'views_id': {'ref': "crm_yziact.action_com_tree"},
                "target": 'current',
            }

        return action


    def change_date_action(self, date):
        date_action = self.last_action

        if not date_action or date > date_action:
            return self.write({'last_action':date})


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    ######RELATIONEL####
    company_id = fields.Many2one(comodel_name='res.partner', string=u"Société", domain="[('company_type','=','company')]", track_visibility="always",related="action_id.company_id", store=True)
    contact_id = fields.Many2one(comodel_name='res.partner', string=u"Contact", domain="[('company_type','=','person'), ('parent_id','=',company_id)]",related="action_id.contact_id", store=True)

    action_id = fields.Many2one(comodel_name='crm_yziact.action')

    @api.multi
    def unlink(self, can_be_deleted=True):
        yzi_action_env = self.env['crm_yziact.action']
        context = {}

        if self._context:
            context = self._context

        for event in self:
            yzi_action = yzi_action_env.search([('event_id.id', '=', event.id)])

            if not context.get('action', False):
                if yzi_action:
                    yzi_action.event_id = ''
                    yzi_action.with_context(event=True).unlink()

            super(CalendarEvent, event).unlink(can_be_deleted)


    @api.multi
    def write(self, vals):
        print(vals.get('start'))
        if vals.get('start'):
            # yzi_action_env = self.env['crm_yziact.action']
            # yzi_action = yzi_action_env.search([('event_id', '=', self.id)])

            if self.action_id and vals.get('start') != self.action_id.date:
                self.action_id.write({'date': vals.get('start')})
        res = super(CalendarEvent, self).write(vals)


        return res


    @api.model
    def create(self, vals):
        res = super(CalendarEvent, self).create(vals)
        if not vals.get('action_id', False):
            action = self.env['crm_yziact.action']
            dict_action = {
                'name':vals.get('name',False),
                'company_id': vals.get('company_id', False),
                'contact_id': vals.get('contact_id', False),
                'type':3,
                'event_id': res.id,
                'user_id':res.user_id.id,
            }

            action_id = action.create(dict_action)
            res.action_id = action_id.id

        return res


    @api.multi
    def action_open_crm_action(self):
        action = False
        if self.action_id:
            action = {
                "type": "ir.actions.act_window",
                "name": "Action Commerciales",
                "res_model": "crm_yziact.action",
                "view_type": 'form',
                "views": [[False, "form"]],
                "domain": [('contact_id', '=', self.id)],
                "res_id":self.action_id.id,
                'views_id': {'ref': "crm_yziact.action_com_form"},
                "target": 'current',
            }

        return action
