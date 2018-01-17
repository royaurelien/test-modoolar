
from odoo import api, models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    horaires_livraison = fields.Text(string="Jours et horaires de livraisons")
