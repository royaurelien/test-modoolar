
import logging
from odoo import api, models, fields

_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
    """ add price_reduce to invoice """

    _inherit = 'account.invoice.line'

    price_reduce = fields.Float(compute='_compute_price_reduce')

    @api.depends('price_unit', 'discount')
    def _compute_price_reduce(self):

        for record in self:

            price_reduce = record.price_unit
            try:
                # 0 <= discount_dec <= 1
                discount_dec = record.discount / 100
                price_reduce = record.price_unit - (record.price_unit * discount_dec)
            except ZeroDivisionError:
                _logger.warning('Impossible de calculer price_reduce de la facture (discount_dec = 0)')

            record.price_reduce = price_reduce
