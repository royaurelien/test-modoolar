# -*- coding:utf-8 -*-

from odoo import models, api, fields
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    no_remise = fields.Boolean(string='ne pas appliquer la remise de pied page')
