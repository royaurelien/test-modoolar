# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class FamilleClient(models.Model):
    _name = 'dom.type_tier'

    #### TEXT ####
    name = fields.Char(string="Nom")

