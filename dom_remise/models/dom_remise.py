# -*- coding:utf-8 -*-

from odoo import models, api, fields
from odoo.exceptions import ValidationError

class DomRemise(models.Model):
    _name = 'dom.remise'

    #### NUMERIQUE #####
    amount = fields.Float(string="Montant")

    #### TEXT #####
    name = fields.Char('Nom', compute='_get_amount_name', store=True)

    #### CONSTRAINS #####
    @api.constrains('amount')
    def _check_amount(self):
        remise_env = self.env['dom.remise']

        for remise in self :
            print(remise.amount)
            if remise.amount<0 or remise.amount>100:
                raise ValidationError("La remise doit être comprise entre 0 et 100")

            exist = remise_env.search([('amount', '=', remise.amount),('id','!=',remise.id)])

            if exist:
                raise ValidationError("Cette remise existe déjà")



    #### COMPUTE #####
    @api.depends('amount')
    def _get_amount_name(self):
        for remise in self:
            remise.name = str(remise.amount)
