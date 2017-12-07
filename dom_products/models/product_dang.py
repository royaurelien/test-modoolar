# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError, RedirectWarning, except_orm
from odoo.tools import pycompat

class ProductDang(models.Model):

    _name = 'product.dang'

    # designation = fields.Text(u'Désignation')
    # description = fields.Text('Description')
    name = fields.Text('Description')

    pg = fields.Selection([
        ('II', 'II'),
        ('III', 'III')
    ], string='PG')

    classe = fields.Selection([
        ('8', '8'),
        ('9', '9'),
        ('3', '3')
    ], string='classe')

    num_danger = fields.Selection([
        ('80', '80'),
        ('86', '86'),
        ('90', '90'),
        ('30', '30'),
        ('33', '33'),
        ('NON DANGEUREUX', 'NON DANGEUREUX')
    ], string='num. danger')
