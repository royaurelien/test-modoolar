# -*- coding: utf-8 -*-

from odoo import models, api, fields, _

# import logging
# _logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one('res.partner', delegate=True)


class SaleReport(models.Model):
    _inherit = 'sale.report'

    partner_id = fields.Many2one('res.partner', delegate=True)

    # Test
    # requested_date = fields.Datetime(related='sale.order')
    requested_date_ = fields.Many2one("sale.order",  delegate=True, read_only=True)
    #amount_total = fields.Float(related='sale.order', read_only=True)
    #picking_ids = fields.Many2one(related='sale.order', inverse='get_true')
    #invoice_status = fields.Char(related="invoice_ids.state", string="statut commande", read_only="True")

    def get_true(self):
        return True


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    partner_id = fields.Many2one('res.partner', delegate=True)

"""
class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    partner_id = fields.Many2one('res.partner', delegate=True)
"""
