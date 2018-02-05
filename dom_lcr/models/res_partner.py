
from odoo import api, models, fields
from odoo.exceptions import UserError
import sys
import logging
logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def get_bank_account(self):
        """
        retourne le compte en banque du res.partner.
        si pas société : retourne le compte en banque du parent
        """
        self.ensure_one()

        account = 0
        # company_type is 'company' or 'person'
        if self.company_type == 'company' :
            if self.bank_ids:
                account = self.bank_ids[0]
        else :
            if self.parent_id :
                if self.parent_id.bank_ids :
                    account = self.parent_id.bank_ids[0]
            else :
                if self.bank_ids:
                    account = self.bank_ids[0]

        if not account:
            raise UserError("Compte en banque non résolu "
                "pour partenaire {}, id {}".format(self.name, self.id))

        return account

"""
partners = self.env['res.partner'].search([])
"""
