
from odoo import api, models

class ParticularReport(models.AbstractModel):
    # _name = 'report.sale.report_name'
    _name = 'report.dom_reports.dom_sale_order_report'
    # _name = 'report.sale.report_saleorder'

    @api.multi
    def render_html(self, data=None):
        import pudb; pudb.set_trace()
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('module.report_name')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('dom_reports.dom_sale_order_report', docargs)
