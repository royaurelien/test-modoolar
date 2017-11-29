# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError, RedirectWarning, except_orm
from odoo.tools import pycompat

import logging
logger = logging.getLogger(__name__)

class ProductFamily(models.Model):

    _name = 'product.family'

    name = fields.Char(string="Nom")
    libelle = fields.Char(string=u"Libellé")

    def name_get(self):

        res = []

        for rec in self:
            res.append((rec.id, rec.name + ' - ' + rec.libelle))

        return res
