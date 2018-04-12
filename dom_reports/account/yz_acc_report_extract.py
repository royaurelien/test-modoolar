# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError
import base64

class YzAccReportExtract(models.TransientModel):
    _name = "yz.acc.report.extract"

    #### DATE ####
    date_debut = fields.Date()
    date_fin = fields.Date()

    #### RELATION ####
    account_id = fields.Many2one('account.account', string='Account')

    #### TEXTE ####
    filename = fields.Char(string='Filename', size=256, readonly=True)

    #### BINAIRE ####
    value = fields.Binary(readonly=True)

    @api.multi
    def action_export(self, date_deb, date_f, account):
        """
        :param date_deb: date de debut pour la selection
        :param date_f: date de fin pour la selection
        :param account: compte a utiliser pour la selection
        :return liste des lignes a afficher sur le report
        """

        account_move_env = self.env['account.move.line']                                                                                # Recuperation du modele
        data_move_line = account_move_env.search([('date', '>=', date_deb), ('date', '<=', date_f), ('account_id', '=', account.id)])   # Selection des lignes a afficher sur le pdf

        return data_move_line

    @api.multi
    def action_export_extract(self):
        """
        :return une action act_url pour telecharger le pdf
        """

        if self.date_debut > self.date_fin:
            raise UserError(_('La date de début doit être inférieure ou égale à la date de fin.'))
        else:
            data_move_lines = self.action_export(self.date_debut, self.date_fin, self.account_id)       # Selection des lignes a afficher


            # Recuperation des ids de chaque ligne a afficher
            docids = []

            for move in data_move_lines:
                docids.append(move.id)


            # Recuperation du template a utiliser
            report_obj = self.env['ir.actions.report']
            report = report_obj._get_report_from_name('dom_reports.dom_report_account_line')


            # Dictionnaire indiquant les lignes a afficher
            docargs = {
                'doc_ids': docids,
                'doc_model': report.model,
                'docs': data_move_lines,
            }

            html = report.render_qweb_html(docids, docargs)                                             # Generation du document sous forme html

            bodies, res_ids, header, footer, specific_paperformat_args = report._prepare_html(html[0])  # Division du html en differentes parties

            mu = report._run_wkhtmltopdf(bodies, header, footer, specific_paperformat_args)             # Assemblage des parties et generation du pdf


            # Encodage du pdf et determination du nom de fichier
            self.write({
                'value': base64.encodestring(mu),
                'filename': 'Extrait de compte',
             })


            # Ouverture de la fenetre de telechargement du pdf
            return {
                     "type": "ir.actions.act_url",
                     "url": "web/content/?model=yz.acc.report.extract&id=" + str(
                         self.id) + "&filename_field=filename&field=value&download=true&filename=%s.pdf" % ('Extrait de compte'),
                     "target": "new",
             }


