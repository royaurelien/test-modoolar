#-*- coding:utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_delivery = fields.Boolean(string="ligne de livraison")

    def _create_delivery_line(self, carrier, price_unit):
        sol = super(SaleOrder, self)._create_delivery_line(carrier, price_unit)
        print(sol)

        return sol


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)

        res['is_delivery'] = self.is_delivery

        return res

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    is_delivery = fields.Boolean(string="ligne de livraison")
