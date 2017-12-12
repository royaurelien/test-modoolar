
from odoo import api, models

class MarketingInfo(object):

    def __init__(self, top_message, fl1, fl2, fl3, fl4):
        self.top_message = top_message
        self.fl1 = fl1
        self.fl2 = fl2
        self.fl3 = fl3
        self.fl4 = fl4

def get_marketing_info(record):

        top_message = record.env['ir.config_parameter'].sudo(
        ).get_param('dom_reports.top_message')

        fl1 = record.env['ir.config_parameter'].sudo(
        ).get_param('dom_reports.footer_logo_1')

        fl2 = record.env['ir.config_parameter'].sudo(
        ).get_param('dom_reports.footer_logo_2')

        fl3 = record.env['ir.config_parameter'].sudo(
        ).get_param('dom_reports.footer_logo_3')

        fl4 = record.env['ir.config_parameter'].sudo(
        ).get_param('dom_reports.footer_logo_4')

        return MarketingInfo(top_message, fl1, fl2, fl3, fl4)


class ReportSaleOrder(models.AbstractModel):
    _name = 'report.dom_reports.dom_report_saleorder'

    @api.multi
    def get_report_values(self, docids, data=None):
        sorders = self.env['sale.order'].browse(docids)
        market_info = get_marketing_info(self)

        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'data': data,
            'docs': sorders,
            'market_info': market_info,
        }


class ReportInvoice(models.AbstractModel):
    _name = 'report.dom_reports.dom_report_invoice'

    @api.multi
    def get_report_values(self, docids, data=None):
        invoices = self.env['account.invoice'].browse(docids)
        market_info = get_marketing_info(self)

        return {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'data': data,
            'docs': invoices,
            'market_info': market_info,
        }


class ReportBL(ReportInvoice):
    # _name = 'report.sale.report_name'
    # report NAME, not its ID...
    _name = 'report.dom_reports.dom_report_bl'

    @api.multi
    def get_report_values(self, docids, data=None):
        invoices = self.env['stock.picking'].browse(docids)
        market_info = get_marketing_info(self)

        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'data': data,
            'docs': invoices,
            'market_info': market_info,
        }
