# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Nope, forbidden ! this is not an inheritance, there are new fields, overriding olds and not defined any more.
    date_order = fields.Date(default=fields.Date.today)
    requested_date = fields.Date()
    validity_date = fields.Date()
    commitment_date = fields.Date(compute='_compute_commitment_date')
    effective_date = fields.Date(compute='_compute_picking_ids')
    confirmation_date = fields.Date()

    partner_centrale_id = fields.Many2one(comodel_name="res.partner", string="Centrale")

    @api.onchange('partner_id')
    def onchange_partner_id_centrale(self):
        self.partner_centrale_id = self.partner_id.centrale_id.id

    @api.multi
    @api.depends('invoice_ids', 'amount_total', 'invoice_status')
    def get_residual(self):
        for order in self:
            residual = order.amount_total
            invoiced = 0.0
            for invoice in order.invoice_ids:
                invoiced += invoice.amount_total_signed

            order.residual = residual - invoiced
        """
        residual_qty = 0
        for line in order.order_line:
            if line.product_uom_qty >= line.qty_invoiced:
                residual_qty += line.product_uom_qty - line.qty_invoiced
            else :
                residual_qty += 0
        """

    residual = fields.Monetary(string=u'Montant dû', compute='get_residual', store=True, track_visibility='onchange')

    @api.onchange('user_id')
    def onchange_user_id(self):
        self.team_id = self.user_id.sale_team_id

    @api.depends('date_order', 'order_line.customer_lead')
    def _compute_commitment_date(self):
        """Compute the commitment date"""
        for order in self:
            dates_list = []
            order_datetime = fields.Datetime.from_string(order.date_order)
            for line in order.order_line.filtered(lambda x: x.state != 'cancel'):
                if order_datetime:
                    dt = order_datetime + timedelta(days=line.customer_lead or 0.0)
                    dates_list.append(dt)
            if dates_list:
                commit_date = min(dates_list) if order.picking_policy == 'direct' else max(dates_list)
                order.commitment_date = fields.Datetime.to_string(commit_date)

