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


    @api.model
    def create(self, vals):
        """
        Le quick_create de odoo remplit le nom or nous souhaitons que ce soit le montant qui soit renseigne

        :param vals: dict de valeurs
        :return: record
        """

        if  'amount' not in vals:
            name = vals.get('name')
            if not name:
                raise ValidationError("Saisie incorrecte")

            try :
                amount = float(name.replace(',', '.'))
            except:
                raise ValidationError("Saisie incorrecte")

            vals['amount'] = amount

        res = super(DomRemise, self).create(vals)

        return res
