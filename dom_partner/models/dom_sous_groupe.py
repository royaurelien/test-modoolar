#-*- coding:utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.exceptions import UserError


class DomSousGroupe(models.Model):
    _name = 'dom.sous.groupe'

    name = fields.Char(u'Nom')
