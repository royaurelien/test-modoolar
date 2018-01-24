# -*- coding:utf-8 -*-

from odoo import models, api, fields

class InvoiceTarif(models.Model):
    _inherit = 'account.invoice'

    #### RELATIONEL #####
    remise = fields.Many2one(comodel_name='dom.remise', string='Remise pied de page (%)')

    #### NUMERIQUE #####
    amount_ht_net = fields.Float('Total HT net', compute='_compute_amount',store=True, track_visibility='onchange')

    @api.onchange('remise')
    def onchange_remise(self):
        vals = self.onchange_remise_values(self.remise)
        self.update(vals)

        self.invoice_line_ids._compute_price()
        self.tax_line_ids._compute_amount_total()

    def onchange_remise_values(self, remise):
        vals = {}
        if remise:
            vals['remise'] = remise

        return vals

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


    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        for line in self.invoice_line_ids:
            remise = 0
            if not line.no_remise:
                remise = line.invoice_id.remise.amount

            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price_unit = price_unit - price_unit * (remise / 100)
            print(price_unit)

            taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']
            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                print(val)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']


        return tax_grouped


class InvoiceTarifLine(models.Model):
    _inherit = 'account.invoice.line'

    price_subtotal_net = fields.Monetary(string='Sous-total net', compute='_compute_price', store=True)

    #### BOOLEAN #####
    no_remise = fields.Boolean(string='ne pas appliquer la remise', related='product_id.no_remise')

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

            if not line.no_remise:
                if line.invoice_id.remise:
                    remise = line.invoice_id.remise.amount

                    price_subtotal = line.price_subtotal - line.price_subtotal * (remise / 100)

                    price_total = line.price_total - line.price_total * (remise / 100)

                    vals['price_subtotal'] = price_subtotal
                    vals['price_total'] = price_total

            line.update(vals)

"""

class InvoiceTarifTax(models.Model):
    _inherit = 'account.invoice.tax'

    @api.depends('amount', 'amount_rounding')
    def _compute_amount_total(self):
        super(InvoiceTarifTax, self)._compute_amount_total()

        for tax_line in self:
            if tax_line.invoice_id.remise:
                remise = tax_line.invoice_id.remise.amount

                tax_line.amount_total = tax_line.amount_total - tax_line.amount_total * (remise / 100)
"""

