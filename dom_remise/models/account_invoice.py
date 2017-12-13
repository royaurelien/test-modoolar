# -*- coding:utf-8 -*-

from odoo import models, api, fields

class InvoiceTarif(models.Model):
    _inherit = 'account.invoice'

    #### RELATIONEL #####
    remise = fields.Many2one(comodel_name='dom.remise', string='Remise (%)')
    
    #### NUMERIQUE #####
    amount_ht_net = fields.Float('Total HT net', compute='_compute_amount',store=True, track_visibility='onchange')
    
    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        for invoice in self:
            super(InvoiceTarif, invoice)._compute_amount()
            amount_ht_net = 0
            for line in invoice.invoice_line_ids:
                amount_ht_net += line.price_subtotal_net

            invoice.amount_ht_net = amount_ht_net


class InvoiceTarifLine(models.Model):
    _inherit = 'account.invoice.line'

    price_subtotal_net = fields.Monetary(string='Sous-total net', compute='_compute_price', store=True)

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice')
    def _compute_price(self):
        super(InvoiceTarifLine, self)._compute_price()
        for line in self :
            currency = line.invoice_id and line.invoice_id.currency_id or None
            vals = {}
            price_subtotal_net = line.price_subtotal
            vals['price_subtotal_net'] = price_subtotal_net

            if line.invoice_id.remise:
                remise = line.invoice_id.remise.amount

                price_subtotal = line.price_subtotal - line.price_subtotal * (remise / 100)

                price_total = line.price_total - line.price_total * (remise / 100)

                vals['price_subtotal'] = price_subtotal
                vals['price_total'] = price_total

            line.update(vals)

class InvoiceTarifTax(models.Model):
    _inherit = 'account.invoice.tax'

    @api.depends('amount', 'amount_rounding')
    def _compute_amount_total(self):
        super(InvoiceTarifTax, self)._compute_amount_total()

        for tax_line in self:
            if tax_line.invoice_id.remise:
                remise = tax_line.invoice_id.remise.amount

                tax_line.amount_total = tax_line.amount_total - tax_line.amount_total * (remise / 100)
