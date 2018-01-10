# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class PlvClient(models.Model):
    _name = 'dom.plv'

    #### TEXT ####
    name = fields.Char(string="Nom")
