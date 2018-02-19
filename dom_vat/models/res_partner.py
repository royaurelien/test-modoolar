from odoo import api, models, fields
import logging
_log = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    """
    this comes from base_vat, this is the TVA simple check
    """
    @api.model
    def simple_vat_check(self, country_code, vat_number):
        _log.warning('stub of simple_vat_check')
        return True

    """
    this comes from base_vat_autocomplete, sets the adress
    """
    @api.onchange('vat')
    def vies_vat_change(self):
        _log.warning('stub of vies_vat_onchange')
        return
