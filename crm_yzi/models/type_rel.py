# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date

class TypeRel(models.Model):
    _name = 'crm_yzi.type_rel'

    name = fields.Char(string='Nom')
