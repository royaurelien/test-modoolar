# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.exceptions import UserError
from datetime import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'


    # A la creation d'un contact, on initialise pas ses comptes client et fournisseur
    property_account_payable_id = fields.Many2one(required=False, default='False')
    property_account_receivable_id = fields.Many2one(required=False, default='False')

    # Reference interne du contact, generee automatiquement
    ref = fields.Char(readonly=True, store=True)


    #### REF INTERNE ####
    def action_get_ref(self):
        return self.get_ref()


    def get_nextseq(self):
        return self.env['ir.sequence'].get('res.partner')



    def get_ref(self):
        for partner in self:
            if not partner.ref:
                ref = partner.get_nextseq()
                if partner.dep_id:
                    num = partner.dep_id.number
                    ref = num + ref
                elif partner.zip and len(partner.zip) >= 2:
                    ref = partner.zip[:2]+ref
                else :
                    ref = '00' + ref

                partner.ref = ref

        return True

    #### ACCOUNT ####

    @api.multi
    def action_create_accounts(self):
        self.action_create_account_customer()
        self.action_create_account_supplier()

        return True


    @api.multi
    def action_create_account_customer(self):
        account_obj = self.env['account.account']

        for partner in self:

            if partner.customer:
                if not partner.ref:
                    raise UserError(u"Veulliez créer une référence à votre client ")

                if not partner.property_account_receivable_id:
                    # Creation du compte client
                    account_s = account_obj.create({"name": "Client - " + partner.name,
                                                    "code": "411" + partner.ref,
                                                    "user_type_id": 1,
                                                    "reconcile": True,
                                                    })
                    partner.property_account_receivable_id = account_s.id

            return True


    @api.multi
    def action_create_account_supplier(self):
        account_obj = self.env['account.account']

        for partner in self:
            if partner.supplier:
                if not partner.ref:
                    raise UserError(u"Veulliez créer une référence à votre fournisseur ")
                if not partner.property_account_payable_id:
                    # Creation du compte fournisseur avec la reference du contact
                    account_p = account_obj.create({"name": "Fournisseur - " + partner.name,
                                                    "code": "401" + partner.ref,
                                                    "user_type_id": 2,
                                                    "reconcile": True,
                                                    })
                    partner.property_account_payable_id = account_p.id
