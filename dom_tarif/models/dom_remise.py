# -*- coding:utf-8 -*-

from odoo import models, api, fields

class DomRemise(models.Model):
    _name = 'dom.remise'

    #### NUMERIQUE #####
    amount = fields.Float(string="Montant")
