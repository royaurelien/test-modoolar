
# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError, RedirectWarning, except_orm
from odoo.tools import pycompat

import logging
logger = logging.getLogger(__name__)

class ProductCategory(models.Model):

    _inherit = 'product.category'

    libelle = fields.Char(string=u"Libellé de la catégorie")

    def name_get(self):

        res = []

        for rec in self:
            name = rec.name if rec.name else ''
            libelle = ' - ' + rec.libelle if rec.libelle else ''
            res.append((rec.id, name + libelle))

        return res
