
from odoo import models, fields, api

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    stock_value = fields.Float(related="product_id.stock_value")
