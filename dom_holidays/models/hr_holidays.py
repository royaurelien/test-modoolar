from odoo import models, fields, api, _

class Holidays(models.Model):
    _inherit = 'hr.holidays'

    @api.onchange('date_from')
    def onchange_date_from(self):
        if self.date_from:
            date_from_splited = self.date_from.split(" ")
            self.date_from = date_from_splited[0] + " 08:00:00"

    @api.onchange('date_to')
    def onchange_date_to(self):
        if self.date_to:
            date_to_splited = self.date_to.split(" ")
            self.date_to = date_to_splited[0] + " 18:00:00"
