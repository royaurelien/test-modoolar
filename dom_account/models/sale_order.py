# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        """
        a partner become a True customer when he confirm his first order with us.
        So we need to give him a ref and a customer account
        :return: super
        """
        rel_id = False
        rel_env = self.env['crm_yzi.type_rel']
        rel = rel_env.search([('name','=','Client')],limit=1)

        if rel:
            rel_id = rel.id

        for order in self:
            if order.partner_id :
                partner = order.partner_id
                partner.write({'type_rel':rel_id})
                partner.get_ref()
                partner.action_create_account_customer()

        return super(SaleOrder, self).action_confirm()
