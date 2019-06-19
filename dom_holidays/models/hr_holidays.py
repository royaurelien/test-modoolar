from odoo import models, fields, api, _
import datetime

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

    @api.model
    def create(self, vals):
        hr = super(Holidays, self).create(vals)

        self.env['mail.activity'].create({
            'activity_type_id': 4,
            'res_name': hr.display_name,
            'summary': "Congé",
            'user_id': 1,
            'res_id': hr.id,
            'res_model': 'hr.holidays',
            'res_model_id': self.env['ir.model'].search([('model', '=', 'hr.holidays')]).id,
            'state': 'planned',
            'date_deadline': datetime.datetime.strptime(hr.date_from, '%Y-%m-%d %H:%M:%S').date(),
            'note': "<p>%s a posé un congé du %s au %s</p>" % (hr.employee_id.name, hr.date_from, hr.date_to)
        })

        return hr
