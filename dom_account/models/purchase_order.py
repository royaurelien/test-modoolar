# -*- coding: utf-8 -*-
from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_centrale_id = fields.Many2one(comodel_name="res.partner", string="Centrale")

    @api.onchange('partner_id')
    def onchange_partner_id_centrale(self):
        self.partner_centrale_id = self.partner_id.centrale_id.id

    @api.multi
    def button_confirm(self):
        """
        a partner become a True supplier when we confirm our first purchase with him.
        So we need to give him a ref and a supplier account
        :return: super
        """
        rel_id = False
        rel_env = self.env['crm_yzi.type_rel']
        rel = rel_env.search([('name', '=', 'Fournisseur')], limit=1)

        if rel:
            rel_id = rel.id

        for purchase in self:
            if purchase.partner_id:
                partner = purchase.partner_id
                partner.write({'type_rel':rel_id})
                partner.get_ref()
                partner.action_create_account_supplier()

        return super(PurchaseOrder, self).button_confirm()

