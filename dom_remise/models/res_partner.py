# -*- coding:utf-8 -*-

from odoo import models, api, fields

class PartnerTarif(models.Model):
    _inherit = 'res.partner'

    #### RELATIONEL #####
    remise = fields.Many2one(comodel='dom.remise', string='Remise (%)')
