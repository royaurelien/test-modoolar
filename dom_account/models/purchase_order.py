# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_confirm(self):
        """
        a partner become a True supplier when we confirm our first purchase with him.
        So we need to give him a ref and a supplier account
        :return: super
        """

        for purchase in self:
            if purchase.parnter_id:
                partner = purchase.parnter_id
                partner.write({'type_rel':'fournisseur'})
                partner.get_ref()
                partner.action_create_account_supplier()

        return super(PurchaseOrder, self).button_confirm()

