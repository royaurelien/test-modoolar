# -*- coding:utf-8 -*-

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    #### RELATIONEL #####
    account_id = fields.Many2one(comodel_name='account.account', string='Compte pour note de frais')
