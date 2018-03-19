# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, AccessError

from odoo import models, api, fields
# from lxml import etree


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.onchange('line_ids', 'line_ids.cout_global')
    def _compute_total(self):
        total = 0.0
        for line in self.line_ids:
            total += line.cout_global

        self.total = total

    company_id = fields.Many2one('res.company', related='location_id.company_id',
                                 required=True, select=True, readonly=True,
                                 states={'draft': [('readonly', False)]})

    total = fields.Float('Total', compute=_compute_total)



    @api.multi
    def action_compute_cout(self):
        for inventory in self:
            for line in inventory.line_ids:
                line._compute_cout()

            inventory._compute_total()


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'
    _order = 'emplacement, emplacement_atom'

    #### NUMERIQUE #####
    cout = fields.Float('Cout', type='float', compute='_compute_cout', store=True)
    cout_global = fields.Float('Cout global', compute='_compute_cout', type='float', store=True)

    #### TEXT #####
    emplacement = fields.Char('Emplacement')
    emplacement_atom = fields.Char('Emplacement')

    #### RELATIONEL #####
    company_id = fields.Many2one('res.company')


    @api.depends('product_id', 'product_qty')
    def _compute_cout(self):

        for line in self:
            line.cout = line.product_id.product_tmpl_id.standard_price

            if line.product_qty >= 0:
                line.cout_global = line.product_id.product_tmpl_id.standard_price * line.product_qty
            else:
                line.cout_global = 0
