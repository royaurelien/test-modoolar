# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.depends('invoice_ids', 'amount_total','invoice_status')
    def get_residual(self):
        for order in self:
            residual = order.amount_total
            invoiced = 0.0
            for invoice in order.invoice_ids:
                invoiced += invoice.amount_total_signed

            order.residual = residual - invoiced
        """
        residual_qty = 0
        for line in order.order_line:
            if line.product_uom_qty >= line.qty_invoiced:
                residual_qty += line.product_uom_qty - line.qty_invoiced
            else :
                residual_qty += 0
        """

    residual = fields.Monetary(string=u'Montant dû', compute='get_residual', store=True, track_visibility='onchange')
