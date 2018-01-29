# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class FamilleClient(models.Model):
    _name = 'dom.famille'

    #### TEXT ####
    code = fields.Char(string="Code")
    name = fields.Char(string="Nom")

    #### RELATIONNEL ####
    property_product_pricelist = fields.Many2one('product.pricelist', string='liste de prix')


class FamilleFournisseur(models.Model):
    _name = 'dom.famille_supplier'

    #### TEXT ####
    # code = fields.Char(string="Code")
    name = fields.Char(string="Nom")
