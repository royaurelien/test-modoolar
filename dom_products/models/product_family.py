# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError, RedirectWarning, except_orm
from odoo.tools import pycompat

class ProductFamily(models.Model):

    _name = 'product.family'

    name = fields.Char(string="Nom")
    libelle = fields.Char(string=u"Libellé")
