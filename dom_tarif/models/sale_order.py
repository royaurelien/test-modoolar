# -*- coding:utf-8 -*-

from odoo import models, api, fields

class SaleTarif(models.Model):
    _inherit = 'sale.order'

    """system de remise globale en pied de page"""

    #### RELATIONEL #####
    remise = fields.Many2one(comodel='dom.remise', string='Remise (%)')

    #### NUMERIQUE #####
    amount_ht_net = fields.Float('Total HT net', compute='_amount_all',store=True, track_visibility='onchange')

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = {}
        res = super(SaleTarif, self).onchange_partner_id()

        if not self.partner_id:
            res['remise'] = False
        else:
            res['remise'] = self.partner_id.remise and self.partner_id.remise.id or False

        self.update(res)


    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            super(SaleTarif, order)._amount_all()
            order._compute_remise_amount()


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


    @api.multi
    def _prepare_invoice(self):
        res = super(SaleTarif, self)._prepare_invoice()

        if self.remise:
            res['remise'] = self.remise and self.remise.id or False

        return res
