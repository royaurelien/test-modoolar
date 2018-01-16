# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        """
                a partner become a True customer when he confirm his first order with us.
                So we need to give him a ref and a customer account
                :return: super
                """
        for order in self:
            if order.partner_id :
                partner = order.partner_id
                partner.write({'type_rel':'client'})
                partner.get_ref()
                partner.action_create_account_customer()

        return super(SaleOrder, self).action_confirm()
