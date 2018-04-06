from odoo import api, models, fields

class YzAccReportExtract(models.TransientModel):
    _name = "yz.acc.report.extract"

    date_debut = fields.Date()
    date_fin = fields.Date()
    account_id = fields.Many2one('account.account', string='Account')

    @api.multi
    def action_export(self, date_deb, date_f, account):
        account_move_env = self.env['account.move.line']
        data_move_line = account_move_env.search([('date', '>=', date_deb), ('date', '<=', date_f), ('account_id', '=', account.id)])

        return data_move_line

    @api.multi
    def action_export_extract(self):
	
        #data_move_lines = self.action_export(self.date_debut, self.date_fin, self.account_id)

        #self.env.ref('dom_reports.dom_report_account_line').report_action(self, data=data_move_lines, config=False)
        
        context = self._context or {}

        data = {}

        data['ids'] = context.get('active_ids', [])

        data['model'] = context.get('active_model', 'ir.ui.menu')

         

        return self.env['ir.actions.report'].report_action('dom_reports.dom_report_account_line', data=data)


class Report(models.AbstractModel):
    _name = 'dom_reports.dom_report_account_line'

    @api.multi
    def get_report_values(self, docids, data=None):

        invoices = self.env['yz.acc.report.extract'].browse(docids)
        market_info = get_marketing_info(self)

        return {
            'doc_ids': docids,
            'doc_model': 'yz.acc.report.extract',
            'data': data,
            'docs': invoices,
            #'market_info': market_info,
        }
        context = self._context or {}

        data = {}

        data['ids'] = context.get('active_ids', [])

        data['model'] = context.get('active_model', 'ir.ui.menu')

         

        return self.env['report'].get_action('custom_module.report_pricelist', data=data)