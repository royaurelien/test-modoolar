# -*- coding:utf-8 -*-

from odoo import models, api, fields
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp

class SaleTarif(models.Model):
    _inherit = 'sale.order'

    """system de remise globale en pied de page"""

    #### RELATIONEL #####
    remise = fields.Many2one(comodel_name='dom.remise', string='Remise (%)')

    #### NUMERIQUE #####
    amount_ht_net = fields.Monetary('Total HT net', compute='_compute_remise_amount',store=True, track_visibility='onchange')

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = {}
        super(SaleTarif, self).onchange_partner_id()

        if not self.partner_id:
            res['remise'] = False
        else:
            res['remise'] = self.partner_id.remise and self.partner_id.remise.id or False

        self.update(res)

    @api.onchange('remise')
    def onchange_remise(self):
        vals = self.onchange_remise_values(self.remise)
        self.update(vals)

        self.order_line._compute_amount()

    def onchange_remise_values(self, remise):
        vals = {}
        if remise:
            vals['remise'] = remise

        return vals


    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            super(SaleTarif, order)._amount_all()
            amount_ht_net = 0
            for line in order.order_line:
                amount_ht_net += line.price_subtotal_net

            order.amount_ht_net = amount_ht_net


    @api.multi
    def _prepare_invoice(self):
        res = super(SaleTarif, self)._prepare_invoice()
        if self.remise:
            res['remise'] = self.remise and self.remise.id or False

        return res


class SaleTarifLine(models.Model):
    _inherit = 'sale.order.line'

    #### NUMERIQUE #####
    price_subtotal_net = fields.Monetary(string='Sous-total net', compute='_compute_amount', store=True)

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'order_id.remise')
    def _compute_amount(self):
        super(SaleTarifLine, self)._compute_amount()
        for line in self:
            vals = {}
            if line.order_id.remise:
                remise = line.order_id.remise.amount

                price_subtotal_net = line.price_subtotal
                price_subtotal = line.price_subtotal - line.price_subtotal * (remise / 100)
                price_tax = line.price_tax - line.price_tax * (remise / 100)
                price_total = line.price_total - line.price_total * (remise / 100)

                vals['price_subtotal_net'] = price_subtotal_net
                vals['price_subtotal'] = price_subtotal
                vals['price_tax'] = price_tax
                vals['price_total'] = price_total

            line.update(vals)
