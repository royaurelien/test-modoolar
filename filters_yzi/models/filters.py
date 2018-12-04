# -*- coding: utf-8 -*-

from odoo import models, api, fields, _, tools

# import logging
# _logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    gr = fields.Many2one('dom.groupe', string='Groupe', related='partner_id.gr')
    sgr = fields.Many2one('dom.sous.groupe', string='Sous Groupe', related='partner_id.sgr')



# class SaleReport(models.Model):
#     _inherit = 'sale.report'
#
#     partner_id = fields.Many2one('res.partner', delegate=True)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    gr = fields.Many2one('dom.groupe', string='Groupe', related='partner_id.gr')
    sgr = fields.Many2one('dom.sous.groupe', string='Sous Groupe', related='partner_id.sgr')