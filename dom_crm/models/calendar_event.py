#-*- coding:utf-8 -*-

from odoo import models, fields, api, exceptions, _

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    def onchange_company_coordonnees(self):
        super(CalendarEvent, self).onchange_company_coordonnees()

        if self.res_model == 'crm.lead' and self.contact_activity_id == False:
            contact = self.env['crm.lead'].browse(self.res_id).partner_id.id
            self.contact_activity_id = contact
