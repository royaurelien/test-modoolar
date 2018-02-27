#-*- coding:utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class DomGroupe(models.Model):
    _name = 'dom.groupe'

    name = fields.Char(u'Nom')
