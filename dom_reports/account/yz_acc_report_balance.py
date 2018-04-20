# -*- coding: utf-8 -*-
from openerp import api, models, fields, _
from openerp.exceptions import UserError
import base64


class YzAccReportBalance(models.TransientModel):
    _name = "yz.acc.report.balance"

    #### DATE ####
    date_debut = fields.Date()
    date_fin = fields.Date()

    #### SELECTION ####
    classe = fields.Selection([('all', 'Toutes les classes'), ('1', 'Classe 1'), ('2', 'Classe 2'), ('3', 'Classe 3'), ('4', 'Classe 4'), ('401', 'Classe 401'), ('411', 'Classe 411'), ('5', 'Classe 5'), ('6', 'Classe 6'), ('7', 'Classe 7')])
    lettre = fields.Selection([('oui', 'Lettré'), ('non', 'Non lettré'), ('deux', 'Les deux')], default='deux')

    #### TEXTE ####
    filename = fields.Char(string='Filename', size=256, readonly=True)

    #### BINAIRE ####
    value = fields.Binary(readonly=True)


    def select_moves_account(self, account):
        """
            :param account: compte pour lequel selectionner les mouvements
            :return une liste de mouvements selon les choix de l'utilisateur
        """

        # On selectionne par compte, entre le debut de l'exercice et la date de fin donnee par l'utilisateur
        if self.lettre == 'oui':                                                                                        # Seulement les ecriture lettrees
            mouvements = self.env['account.move.line'].search([('account_id.id', '=', account.id),
                                                               ('date', '<=', self.date_fin),
                                                               ('date', '>=', self.date_debut),
                                                               ('reconciled', '=', True)])
        elif self.lettre == 'non':                                                                                      # Seulement les ecritures non lettrees
            mouvements = self.env['account.move.line'].search([('account_id.id', '=', account.id),
                                                               ('date', '<=', self.date_fin),
                                                               ('date', '>=', self.date_debut),
                                                               ('reconciled', '=', False)])
        else:                                                                                                           # Toutes les ecritures independamment du lettrage
            mouvements = self.env['account.move.line'].search([('account_id.id', '=', account.id),
                                                               ('date', '<=', self.date_fin),
                                                               ('date', '>=', self.date_debut)])

        return mouvements


    def calcul_debit_credit_account(self, mouvements):
        """
            :param mouvements: les operations sur lesquelles calculer le debit, le credit et les soldes d'un compte
            :return une liste avec le debit et le credit du compte, et une liste avec les soldes du compte
        """

        debit = 0.0
        credit = 0.0

        # Calul du debit et credit du compte
        for mouvement in mouvements:                                                                                    # Addition du debit et credit de chaque mouvement
            debit = debit + mouvement.debit
            credit = credit + mouvement.credit

        # Calcul du solde debiteur et crediteur du compte
        if debit > credit:
            soldes = [debit-credit, 0.0]
        elif debit == credit:
            soldes = [0.0, 0.0]
        else:
            soldes = [0.0, -(debit-credit)]

        return [debit, credit], soldes


    def calcul_totaux_classe(self, dc_classe, classe):
        """
            :param dc_classe: les debits, credits et soldes des comptes d'une classe
            :param classe: la classe sur laquelle on effectue les calculs
            :return les debits et credits totaux, ainsi que les soldes totaux de la classe
        """

        t_debit = 0.0
        t_credit = 0.0
        s_debit = 0.0
        s_credit = 0.0

        # Calcul des totaux de la classe
        for solde in dc_classe:                                                                                         # Addition des debits, credits et soldes de chaque compte de la classe
            t_debit = t_debit + solde[2]
            t_credit = t_credit + solde[3]
            s_debit = s_debit + solde[4]
            s_credit = s_credit + solde[5]

        return [t_debit, t_credit, s_debit, s_credit, classe]


    def calcul_total_general(self, totaux_classes):
        """
            :param totaux_classes: les debits, credits et soldes des classes sur lesquelles on travaille
            :return le debit, le credit et les soldes totaux des classes
        """

        tg_debit = 0.0
        tg_credit = 0.0
        sg_debit = 0.0
        sg_credit = 0.0

        # Calcul des totaux generaux
        for total in totaux_classes:                                                                                    # Addition des debits, credits et soldes totaux de chaque classe
            tg_debit = tg_debit + total[0]
            tg_credit = tg_credit + total[1]
            sg_debit = sg_debit + total[2]
            sg_credit = sg_credit + total[3]

        return [tg_debit, tg_credit, sg_debit, sg_credit]


    def cas411(self):
        """
            :return les debits, credits et soldes pour les comptes en 411, ainsi que le total
        """

        a411 = self.env['account.account'].search([('code', '=like', '411%')])          # Recuperation des comptes en 411

        dc = []

        debit = 0.0
        credit = 0.0

        # Calcul du debit et credit de tous les comptes en 411
        for other in a411:
            mouv = self.select_moves_account(other)
            de_cr, sol = self.calcul_debit_credit_account(mouv)
            debit = debit + de_cr[0]
            credit = credit + de_cr[1]

        # Calcul du solde debiteur et crediteur des comptes 411
        if debit > credit:
            soldesd = debit - credit
            soldesc= 0.0
        elif debit == credit:
            soldesd = 0.0
            soldesc = 0.0
        else:
            soldesd = 0.0
            soldesc = -(debit-credit)

        # Ajout d'une ligne pour les 411
        dc.append(['411', 'Comptes 411', debit, credit, soldesd, soldesc, '411'])

        # Calcul des totaux pour les 411
        totaux_411 = self.calcul_totaux_classe(dc, '411')

        return dc, [totaux_411]


    def cas401(self):
        """
            :return un regroupement des debits, credits et soldes de tous les comptes en 401, et le total
        """

        a401 = self.env['account.account'].search([('code', '=like', '401%')])                                          # Recuperation des comptes en 401

        dc = []

        debit = 0.0
        credit = 0.0

        # Calcul du debit et du credit de tous les comptes 401
        for account in a401:
            mouvements = self.select_moves_account(account)
            de_cr, sol = self.calcul_debit_credit_account(mouvements)
            debit = debit + de_cr[0]
            credit = credit + de_cr[1]

        # Calcul du solde debiteur et crediteur  des comptes 401
        if debit > credit:
            soldesd = debit - credit
            soldesc = 0.0
        elif debit == credit:
            soldesd = 0.0
            soldesc = 0.0
        else:
            soldesd = 0.0
            soldesc = -(debit - credit)

        # Ajout d'une ligne pour les 401
        dc.append(['401', 'Comptes 401', debit, credit, soldesd, soldesc, '401'])

        # Calcul des totaux pour les 401
        totaux_401 = self.calcul_totaux_classe(dc, '401')

        return dc, [totaux_401]


    def cas4(self):
        """
            :return les debits, credits et soldes pour les comptes de la classe 4, avec un regroupement pour les comptes en 401 et 411 (hors 411000), ainsi que le total
        """

        # Recuperation des comptes de la classe 4
        a4 = self.env['account.account'].search([('code', '=like', '4%')])

        # Recuperation des comptes en 401 et 411
        a401 = self.env['account.account'].search([('code', '=like', '401%')])
        a411 = self.env['account.account'].search([('code', '=like', '411%')])

        accounts_others_4 = []
        dc = []

        # Recuperation des comptes de la classe 4 sauf 401 et 411
        for acc in a4:
            if acc not in a401 and acc not in a411:
                accounts_others_4.append(acc)

        # Ajout d'une ligne pour chaque compte de la classe 4
        for account in accounts_others_4:
            mouvements = self.select_moves_account(account)
            de_cr, sol = self.calcul_debit_credit_account(mouvements)
            if de_cr[0] > 0.0 or de_cr[1] > 0.0:
                dc.append([account.code, account.name, de_cr[0], de_cr[1], sol[0], sol[1], '4'])

        s401, t401 = self.cas401()
        s411, t411 = self.cas411()

        # Ajout des lignes de 401, 411, et du compte 411000
        dc.append([s401[0][0], s401[0][1],s401[0][2], s401[0][3], s401[0][4], s401[0][5], '4'])
        dc.append([s411[0][0], s411[0][1],s411[0][2], s411[0][3], s411[0][4], s411[0][5], '4'])

        # Calcul des totaux de la classe 4
        totaux_4 = self.calcul_totaux_classe(dc, '4')

        return dc, [totaux_4]


    def others_case(self,classes):
        """
            :param classes: classes pour lesquelles recuperer des donnees
            :return les debits, credits et soldes des comptes pour les classes demandees, ainsi que le total par classe
        """

        dc = []
        totaux_classes = []

        # Pour chaque classe, on effectue les calculs
        for classe in classes:                                                                                          # Pour chaque classe demandee, on recupere les informations
            # On effectue un traitement different si la classe est la 4
            if classe != '4':
                accounts_classe = self.env['account.account'].search([('code', '=like', str(classe)+'%')])              # Recuperation des comptes de classe en cours

                for account in accounts_classe:                                                                         # Pour chaque compte, on ajoute une ligne
                    mouvements = self.select_moves_account(account)
                    de_cr, sol = self.calcul_debit_credit_account(mouvements)
                    if de_cr[0] > 0.0 or de_cr[1] > 0.0:
                        dc.append([account.code, account.name, de_cr[0], de_cr[1], sol[0], sol[1], classe])

                # Calcul des totaux pour la classe
                pour_total_classe = []

                for m in dc:                                                                                            # On recupere les lignes qu'on a precedemment ajoutees qui sont de la classe en cours
                    if m[6] == classe:
                        pour_total_classe.append(m)

                totaux_classes.append(self.calcul_totaux_classe(pour_total_classe, classe))                             # On effectue les totaux pour la classe
            else:
                # On utilise la methode s'occupant de la classe 4 et on ajoute les soldes et les totaux a nos listes deja existantes
                sol, tot = self.cas4()
                totaux_classes.append(tot[0])

                for solde in sol:
                    dc.append(solde)

        return dc, totaux_classes


    @api.multi
    def action_export_balance(self):
        """
            :return une action act_url pour telecharger le pdf
        """

        # Calcul du debut de l'exercice suivant
        if self.date_debut != False:
            date_debut_split = self.date_debut.split('-')
            date_fin_max = str(int(date_debut_split[0]) + 1) + '-' + str(date_debut_split[1]) + '-' + str(date_debut_split[2])

        if self.date_fin == False or self.date_debut == False or self.date_fin < self.date_debut or self.classe == False or self.date_fin >= date_fin_max:
            raise UserError(_('Vous avez oublié un champ, entré des dates incorectes ou donné une période de temps supérieure à un exercice'))                                                    # Si l'utilisateur ne remplit par tous les champs, on provoque une erreur
        else:
            """
                Utilisation de la bonne methode, selon la demande
                dc est sous forme : [[code, nom, debit, credit, solde debiteur, solde crediteur, classe],[], []...]
                totaux est sous la forme : [[debit total, credit total, solde debiteur total, solde crediteur total, classe], [], []...]
                classes est une liste des classes qu'on veut afficher
            """
            if self.classe == 'all':
                dc, totaux_classes = self.others_case(['1', '2', '3', '4', '5', '6', '7'])
                classes = ['1', '2', '3', '4', '5', '6', '7']

            elif self.classe == '401':
                dc, totaux_classes = self.cas401()
                classes = ['401']

            elif self.classe == '411':
                dc, totaux_classes = self.cas411()
                classes = ['411']

            else:
                dc, totaux_classes = self.others_case([self.classe])
                classes = [self.classe]

            # Accounts et docids vides pour ne pas creer d'erreurs, notamment sur get_pdf
            accounts = self.env['account.account']

            docids = []

            for account in accounts:
                docids.append(account.id)

            # Total general des debits, credits et soldes
            total_gen = self.calcul_total_general(totaux_classes)

            # Donnees pour le report
            docargs = {
                'doc_ids': docids,
                'doc_model': 'account.account',
                'docs': accounts,
                'soldes': dc,
                'infos': self,
                'classes': classes,
                'totaux': totaux_classes,
                'total_gen': total_gen,
            }

            # Recuperation du template a utiliser
            report_obj = self.env['ir.actions.report']
            report = report_obj._get_report_from_name('dom_reports.dom_report_account_line_balance')

            # Creation du PDF
            html = report_obj.render_template('dom_reports.dom_report_account_line_balance', docargs)  # Generation du html
            bodies, res_ids, header, footer, specific_paperformat_args = report_obj._prepare_html(html)  # Division du html en differentes parties
            pdf = report._run_wkhtmltopdf(bodies, header, footer, specific_paperformat_args)  # Assemblage des parties et generation du pdf

            # Enregistrement du PDF et definition de son nom
            self.write({
                'value': base64.encodestring(pdf),
                'filename': 'Balance générale',
            })

            # Ouverture de la fenetre de telechargement du PDF
            return {
                "type": "ir.actions.act_url",
                "url": "web/content/?model=yz.acc.report.balance&id=" + str(
                    self.id) + "&filename_field=filename&field=value&download=true&filename=%s.pdf" % (
                            'Balance générale'),
                "target": "new",
            }
