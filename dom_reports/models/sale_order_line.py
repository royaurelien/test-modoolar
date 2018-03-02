
from odoo import api, models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    comment_predef = fields.Many2one(comodel_name="dom.comment", string="Commentaire Prédéfini")
    comment_free = fields.Html(string="Commentaire Libre")
    comment_position = fields.Selection(selection=[
        ('before', 'Avant la ligne'),
        ('after', 'Après la ligne'),
    ], default='after', string="Position commentaire")

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        name = product.name
        if product.description_sale:
            name += '\n' + product.description_sale

        self.name = name

        return res
