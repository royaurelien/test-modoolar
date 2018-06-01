# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError
import base64
import xlsxwriter
from io import BytesIO

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

    def solde_initial(self, date_deb, account):
        """
            :param date_deb: date maximum des enregistrements
            :param account: compte a utiliser
            :return le solde initial
        """

        lines = self.env['account.move.line'].search([('date', '<', date_deb), ('account_id', '=', account.id)])                        # Récuperation des enregistrements precedant ceux de l'extrait de compte
        solde = 0                                                                                                                       # Initialisation du solde

        # Calcul du solde initial
        for line in lines:
            solde = solde + line.balance

        return solde

    @api.multi
    def operations_export(self, date_deb, date_f, account):
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
            raise UserError(_('La date de début doit être inférieure ou égale à la date de fin.'))          # Retourne une erreur
        else:
            data_move_lines = self.operations_export(self.date_debut, self.date_fin, self.account_id)       # Selection des lignes a afficher

            # Recuperation des ids de chaque ligne a afficher
            docids = []

            for move in data_move_lines:
                docids.append(move.id)

            solde_initial = self.solde_initial(self.date_debut, self.account_id)                            # Recuperation du solde initial

            # Recuperation du template a utiliser
            report_obj = self.env['ir.actions.report']
            report = report_obj._get_report_from_name('dom_reports.dom_report_account_line')

            # Dictionnaire indiquant les lignes a afficher
            docargs = {
                'doc_ids': docids,
                'doc_model': 'account.move.line',
                'docs': data_move_lines,
                'solde': solde_initial,
                'infos': self,
            }

            # Creation du PDF
            html = report_obj.render_template('dom_reports.dom_report_account_line', docargs)            # Generation du html
            bodies, res_ids, header, footer, specific_paperformat_args = report_obj._prepare_html(html)  # Division du html en differentes parties
            pdf = report._run_wkhtmltopdf(bodies, header, footer, specific_paperformat_args)             # Assemblage des parties et generation du pdf


            # Encodage du pdf et determination du nom de fichier
            self.write({
                'value': base64.encodestring(pdf),
                'filename': 'Extrait de compte',
             })

            # Ouverture de la fenetre de telechargement du pdf
            return {
                     "type": "ir.actions.act_url",
                     "url": "web/content/?model=yz.acc.report.extract&id=" + str(
                         self.id) + "&filename_field=filename&field=value&download=true&filename=%s.pdf" % ('Extrait de compte'),
                     "target": "new",
             }

    @api.multi
    def action_export_extract_excel(self):
        """
        :return une action act_url pour telecharger le fichier excel
        """

        if self.date_debut > self.date_fin:
            raise UserError(
                _('La date de début doit être inférieure ou égale à la date de fin.'))  # Retourne une erreur
        else:
            data_move_lines = self.operations_export(self.date_debut, self.date_fin,
                                                     self.account_id)  # Selection des lignes a afficher

            solde_initial = self.solde_initial(self.date_debut, self.account_id)  # Recuperation du solde initial

            data = []
            columns = []

            cumule = solde_initial

            table = 1

            debit = 0.0
            credit = 0.0

            # Calcul des donnees
            for move in data_move_lines:
                cumule += move.balance

                if move.reconciled == True:
                    data.append(
                        [move.date, move.partner_id.name or '', move.move_id.name, move.debit, 'Oui', move.credit,
                         cumule])
                else:
                    data.append(
                        [move.date, move.partner_id.name or '', move.move_id.name, move.debit, 'Non', move.credit,
                         cumule])

                debit += move.debit
                credit += move.credit

                table += 1

            # Creation du fichier
            output = BytesIO()
            workbook = xlsxwriter.Workbook(output)

            ws = workbook.add_worksheet('Extrait de compte')

            # Formats, mise en page
            format = workbook.add_format({'num_format': 0x02})
            format_total = workbook.add_format({'num_format': 0x02, 'bold': True})

            ws.set_column(0, 6, 20)

            # Preparation et creation du tableau
            ws.write(0, 0, 'Solde initial : ')
            ws.write(0, 1, solde_initial, format)

            columns.append({'header': 'Date'})
            columns.append({'header': 'Client'})
            columns.append({'header': 'Num de piece'})
            columns.append({'header': 'Debit', 'format': format})
            columns.append({'header': 'Lettre'})
            columns.append({'header': 'Credit', 'format': format})
            columns.append({'header': 'Solde cumule', 'format': format})

            # Creation d'un tableau pour y placer les informations
            ws.add_table(1, 0, table, 6, {'columns': columns, 'data': data, 'style': 'Table Style Light 1'})

            # Ajout de la ligne de total
            ws.write(table + 1, 0, 'Totaux', format_total)
            ws.write(table + 1, 3, debit, format_total)
            ws.write(table + 1, 5, credit, format_total)
            ws.write(table + 1, 6, '=%f' % (cumule), format_total)

            workbook.close()

            # Enregistrement du fichier et definition de son nom
            self.write({
                'value': base64.encodestring(output.getvalue()),
                'filename': 'Extrait de compte' + '-' + self.date_debut + "/" + self.date_fin,
            })

            # Ouverture de la fenetre de telechargement du PDF
            return {
                "type": "ir.actions.act_url",
                "url": "web/content/?model=yz.acc.report.extract&id=" + str(
                    self.id) + "&filename_field=filename&field=value&download=true&filename=%s.xlsx" % (
                                   'Extrait de compte' + '-' + self.date_debut + "/" + self.date_fin),
                "target": "new",
            }



