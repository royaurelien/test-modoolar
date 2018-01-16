# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'


    @api.model
    def create(self, vals):
        parnter_env = self.env['res.partner']

        if vals.get('partner_id'):
            partner = parnter_env.browse(vals.get('partner_id'))

            if not partner.ref:
                partner.get_ref()

            if not partner.property_account_receivable_id:
                partner.action_create_account_customer()

            if not partner.property_account_payable_id:
                partner.action_create_account_supplier()

        return super(AccountInvoice, self).create(vals)
