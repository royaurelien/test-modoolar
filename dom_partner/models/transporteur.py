# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class Transporteur(models.Model):
    _name = 'dom.transporteur'


    #### TEXT ####
    name = fields.Char(string='Nom')
