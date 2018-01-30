
from odoo import api, models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_comment = fields.Boolean(string="Est un commentaire")
