
from odoo import models, fields, api

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    stock_value = fields.Float(related="product_id.stock_value")

    product_id = fields.Many2one('product.product', delegate=True)
