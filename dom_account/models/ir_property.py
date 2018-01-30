# -*- coding: utf-8 -*-

from odoo.exceptions import AccessError
from odoo import api, fields, models, _


class IrProperty(models.Model):
    _inherit = 'ir.property'


    def set_to_nothing(self):
        self.value_reference = False
