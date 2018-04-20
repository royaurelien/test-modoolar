# -*- coding: utf-8 -*-


# [TODOO]: Trier les imports

from odoo import models, api, fields, _

import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one('res.partner', delegate=True)


class SaleReport(models.Model):
    _inherit = 'sale.report'

    partner_id = fields.Many2one('res.partner', delegate=True)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    partner_id = fields.Many2one('res.partner', delegate=True)

"""
class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    partner_id = fields.Many2one('res.partner', delegate=True)
"""
