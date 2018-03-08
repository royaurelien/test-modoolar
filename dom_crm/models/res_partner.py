#-*- coding:utf-8 -*-

from odoo import models, fields, api, exceptions, _



class ResPartner(models.Model):
    _inherit = 'res.partner'

    CA_objectif = fields.Float('CA Objectif')
    CA_progress = fields.Integer('progess', compute='_compute_ca_progress')



    @api.multi
    def _compute_ca_progress(self):
        for partner in self :
            objective = partner.CA_objectif
            real = partner.ca_12

            if str(objective) == '0.0' or str(real) == '0.0':
                progress = 0
            else:

                progress = int(100.0 * real / objective)

            partner.CA_progress = progress
