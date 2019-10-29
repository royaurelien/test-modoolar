# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class SaleReport(models.Model):
    _inherit = 'sale.report'

    partner_centrale_id = fields.Many2one(comodel_name="res.partner", string="Centrale")
    confirmation_date = fields.Date()
    date = fields.Date()

    def _select(self):
        res = super(SaleReport, self)._select()

        res += ", s.partner_centrale_id as partner_centrale_id"

        return res

    def _group_by(self):
        res = super(SaleReport, self)._group_by()

        res += ", s.partner_centrale_id"

        return res