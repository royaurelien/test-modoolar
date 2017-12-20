
from odoo import api, models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    comment_predef = fields.Many2one(comodel_name="dom.comment", string="Commentaire Prédéfini")
    comment_free = fields.Html(string="Commentaire Libre")
    comment_position = fields.Selection(selection=[
        ('before', 'Avant la ligne'),
        ('after', 'Après la ligne'),
    ], default='after', string="Position commentaire")
