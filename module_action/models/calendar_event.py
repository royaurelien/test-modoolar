# -*- coding:utf-8 -*-

from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta
from operator import itemgetter, attrgetter
import logging
_log = logging.getLogger(__name__)


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
            regarding = ''

            if vals.get('contact_id', False):
                regarding = 'contact'
            if vals.get('company_id', False):
                regarding = 'company'

            dict_action = {
                'name':vals.get('name',False),
                'company_id': vals.get('company_id', False),
                'contact_id': vals.get('contact_id', False),
                'regarding':regarding,
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

    @api.multi
    @api.onchange('contact_id')
    def append_address(self):

        for rec in self:
            partner = rec.contact_id
            if not partner:
                continue

            existing_desc = '{}\n'.format(rec.description) if rec.description else ''
            rec.description = existing_desc + partner.get_formatted_info()
