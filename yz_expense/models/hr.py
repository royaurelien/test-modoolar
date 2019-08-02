# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from openerp.exceptions import UserError

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    ##### RELATIONNEL ####
    vehicule_puissance_fiscale = fields.Many2one('hr.taux_kilometriques', 'Puissance fiscale du vehicule')
    fiscal_position = fields.Many2one('account.fiscal.position', string='Position fiscale')
    account_id = fields.Many2one(comodel_name='account.account', string='Compte pour note de frais')

    ###### TEXT ####
    vehicule_intitule = fields.Char("Description du véhicule")

    
class HrTauxKilometrique(models.Model):
    _name = "hr.taux_kilometriques"
    _description = "Taux kilometriques"

    name = fields.Char('Description du taux', size=128, required=True, select=True)
    cout = fields.Float('Prix')
