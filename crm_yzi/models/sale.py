# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class SaleOrder(models.Model):
    _inherit="sale.order"

    @api.multi
    def print_quotation(self):
        if self.partner_id:
            self.partner_id.change_date(date.today())
        if self.opportunity_id:
            self.opportunity_id.dernier_devis = date.today()

        res = super(SaleOrder, self).print_quotation()

        return res
