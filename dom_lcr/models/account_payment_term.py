
from odoo import api, models, fields
from odoo.exceptions import UserError
import sys
import logging
logger = logging.getLogger(__name__)

class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    is_lcr = fields.Boolean(string="Est un paiement avec LCR")
