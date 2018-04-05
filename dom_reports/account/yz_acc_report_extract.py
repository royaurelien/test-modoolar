from odoo import api, models, fields

class YzAccReportExtract(models.TransientModel):
    _name = "yz.acc.report.extract"
    _inherit = ['account.move.line']

    date_debut = fields.Date()
    date_fin = fields.Date()

