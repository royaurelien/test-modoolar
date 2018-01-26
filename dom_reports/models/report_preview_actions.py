from odoo import api, models, fields
import logging
_log = logging.getLogger(__name__)

"""
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

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def action_preview_report(self):

        # 127.0.0.1:8071/report/pdf/dom_reports.dom_report_saleorder/2
        for rec in self:
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            # record_url = base_url + "/web#id=" + str(self.id) + "&view_type=form&model=WWW&menu_id=XXX&action=YYY"
            record_url = base_url + "/report/pdf/dom_reports.dom_report_com_fourn/" + str(self.id)

        client_action = {
            'type': 'ir.actions.act_url',
            # 'name': "Report Preview",
            'target': 'new',
            'url': record_url,
        }

        return client_action

"""

# https://jeffknupp.com/blog/2013/12/28/improve-your-python-metaclasses-and-dynamic-classes-with-type/
# http://www.mindissoftware.com/Understand-Odoo-Model-Part1/
# odoo/api.py and odoo/models.py
class_info = {
    'SaleOrder': {'model': 'sale.order', 'report_path': 'dom_report_saleorder'},
    'AccountInvoice': {'model': 'account.invoice', 'report_path': 'dom_report_invoice'},
    'StockPicking': {'model': 'stock.picking', 'report_path': 'dom_report_bl'},
    'PurchaseOrder': {'model': 'purchase.order', 'report_path': 'dom_report_com_fourn'},
}

# need to provide the __module__ otherwise it will be odoo.api and won't work
module = 'odoo.addons.dom_reports.models.report_preview_actions'

# instead of making N classes for N preview, we can just fill the dict and this will create
# all our models with the right method to provide the preview for each model/report
for ckey in class_info:
    model = class_info[ckey]['model']
    path = class_info[ckey]['report_path']
    cls = type(ckey, (models.Model,), {'_inherit': model, '__module__': module})

    # need to do this to circumvent late binding of path
    def gen_action_preview_report(path=path):
        def f(self):
            for rec in self:
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                record_url = base_url + "/report/pdf/dom_reports.%s/" % path + str(self.id)

            client_action = {
                'type': 'ir.actions.act_url',
                # 'name': "Report Preview",
                'target': 'new',
                'url': record_url,
            }

            return client_action

        return f

    cls.action_preview_report = gen_action_preview_report()

    # mid = id(cls.action_preview_report)
    # _log.critical("bound method with id : %s to path %s" % (mid, path))

