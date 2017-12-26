from odoo import api, models, fields
import logging
_log = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_preview_report(self):

        # 127.0.0.1:8071/report/pdf/dom_reports.dom_report_saleorder/2
        for rec in self:
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            # record_url = base_url + "/web#id=" + str(self.id) + "&view_type=form&model=WWW&menu_id=XXX&action=YYY"
            record_url = base_url + "/report/pdf/dom_reports.dom_report_saleorder/" + str(self.id)

        client_action = {
            'type': 'ir.actions.act_url',
            # 'name': "Report Preview",
            'target': 'new',
            'url': record_url,
        }

        return client_action

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_preview_report(self):

        # 127.0.0.1:8071/report/pdf/dom_reports.dom_report_saleorder/2
        for rec in self:
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            # record_url = base_url + "/web#id=" + str(self.id) + "&view_type=form&model=WWW&menu_id=XXX&action=YYY"
            record_url = base_url + "/report/pdf/dom_reports.dom_report_invoice/" + str(self.id)

        client_action = {
            'type': 'ir.actions.act_url',
            # 'name': "Report Preview",
            'target': 'new',
            'url': record_url,
        }

        return client_action

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_preview_report(self):

        # 127.0.0.1:8071/report/pdf/dom_reports.dom_report_saleorder/2
        for rec in self:
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            # record_url = base_url + "/web#id=" + str(self.id) + "&view_type=form&model=WWW&menu_id=XXX&action=YYY"
            record_url = base_url + "/report/pdf/dom_reports.dom_report_bl/" + str(self.id)

        client_action = {
            'type': 'ir.actions.act_url',
            # 'name': "Report Preview",
            'target': 'new',
            'url': record_url,
        }

        return client_action
