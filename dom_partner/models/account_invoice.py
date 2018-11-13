# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # fac_mail = fields.Boolean(string='Facture par mail',related='partner_id.fac_mail')
    fac_mail = fields.Boolean(string='Facture par mail', compute='_get_fac_mail')


    @api.multi
    @api.depends('partner_id')
    def _get_fac_mail(self):
        for invoice in self:
            if invoice.partner_id:
                if invoice.partner_id.type == 'invoice':
                    invoice.fac_mail = invoice.partner_id.parent_id.fac_mail

                else:
                    invoice.fac_mail = invoice.partner_id.fac_mail




    # @api.onchange('partner_id', 'company_id')
    # def _onchange_partner_id(self):
    #     res = super(AccountInvoice, self)._onchange_partner_id()
    #
    #     if self.partner_id:
    #
    #         if self.partner_id.type == 'invoice':
    #             res['fac_mail']=self.partner_id.parent_id.fac_mail
    #             # self.update({'fac_mail':self.partner_id.parent_id.fac_mail})
    #
    #         else:
    #             print('TEEEEEEEEESSSSSSSSSSSSSSSSSSSSST')
    #             self.fac_mail = self.partner_id.fac_mail
    #
    #     return res
