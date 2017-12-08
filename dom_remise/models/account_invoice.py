# -*- coding:utf-8 -*-

from odoo import models, api, fields

class InvoiceTarif(models.Model):
    _inherit = 'account.invoice'

    #### RELATIONEL #####
    remise = fields.Many2one(comodel='dom.remise', string='Remise (%)')
    
    #### NUMERIQUE #####
    amount_ht_net = fields.Float('Total HT net', compute='_compute_amount',store=True, track_visibility='onchange')
    
    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        for invoice in self:
            super(InvoiceTarif, invoice)._compute_amount()
            invoice._compute_remise_amount(invoice)

    def _compute_remise_amount(self):
        vals = {}
        vals['amount_ht_net'] = self.amount_untaxed
        remise = self.remise

        if remise:
            amount_untaxed = self.amount_untaxed - self.amount_untaxed * (remise.amount / 100)
            amount_tax = self.amount_tax - self.amount_tax * (remise.amount / 100)
            amount_total = self.amount_total - self.amount_total * (remise.amount / 100)

            vals = {
                'amount_untaxed': self.currency_id.round(amount_untaxed),
                'amount_tax': self.currency_id.round(amount_tax),
                'amount_total': self.currency_id.round(amount_total),
            }

        self.update(vals)

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(InvoiceTarif, self)._onchange_partner_id()

        if self.partner_id:
            self.remise = self.partner_id.remise and self.partner_id.remise.id or False

        return res
