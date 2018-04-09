from odoo import api, models, fields

class YzAccReportExtract(models.TransientModel):
    _name = "yz.acc.report.extract"
    move_account = fields.Many2one('account.move.line')


    date_debut = fields.Date()
    date_fin = fields.Date()
    account_id = fields.Many2one('account.account', string='Account')

    filename_extract = fields.Char(string='Filename', size=256, readonly=True)
    value_extract = fields.Binary(string='Value',readonly=True)

    @api.multi
    def action_export(self, date_deb, date_f, account):
        account_move_env = self.env['account.move.line']
        data_move_line = account_move_env.search([('date', '>=', date_deb), ('date', '<=', date_f), ('account_id', '=', account.id)])

        return data_move_line

    @api.multi
    def action_export_extract(self):
        data_move_lines = self.action_export(self.date_debut, self.date_fin, self.account_id)



        docids = []

        for move in data_move_lines:
            docids.append(move.id)

        report_obj = self.env['ir.actions.report']

        report = report_obj._get_report_from_name('dom_reports.dom_report_account_line')

        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            #'doc_model': 'dom_reports.dom_report_account_line',
            'report_type': report.report_type,
            'docs': self,
        }

        self.filename_extract = 'Extract_test'
        self.value_extract = report.render(docids, docargs)
        name = 'extract'

        action = {
            # 'name': 'ecriture_sage',
            'type': 'ir.actions.act_url',
            'url': "web/content/?model=account.move.line&id=" + str(
                self.id) + "&filename_field=%s&field=%s&download=true&filename=%s.csv" % ('filename_extract', 'value_extract', name),
            'target': 'new',
        }

        return action


