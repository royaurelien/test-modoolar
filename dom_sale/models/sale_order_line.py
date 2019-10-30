# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from datetime import date, datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        # values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        self.ensure_one()
        date_planned = datetime.strptime(self.order_id.confirmation_date, DEFAULT_SERVER_DATE_FORMAT) \
                       + timedelta(days=self.customer_lead or 0.0) - timedelta(
            days=self.order_id.company_id.security_lead)
        values = {
            'company_id': self.order_id.company_id,
            'group_id': group_id,
            'sale_line_id': self.id,
            'date_planned': date_planned.strftime(DEFAULT_SERVER_DATE_FORMAT),
            'route_ids': self.route_id,
            'warehouse_id': self.order_id.warehouse_id or False,
            'partner_dest_id': self.order_id.partner_shipping_id
        }
        return values
