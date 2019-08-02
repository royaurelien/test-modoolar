# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_expensed = fields.Boolean('Peut être inséré dans une note de frais', default=False)
