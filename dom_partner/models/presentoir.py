# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class PresentoirClient(models.Model):
    _name = 'dom.presentoir'

    #### TEXT ####
    name = fields.Char(string="Nom")
