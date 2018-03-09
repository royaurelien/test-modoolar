# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools



class ClassificationONU(models.Model):
    _name = 'dom.classification.onu'

    #### INTEGER #####
    name = fields.Char('Code ONU')
    emballage = fields.Integer('Groupe emballage')

    #### TEXT #####
    description = fields.Char(u'Désignation officielle')
    classification = fields.Char('Classification')

