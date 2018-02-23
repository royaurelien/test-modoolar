# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError, RedirectWarning, except_orm
import csv
from odoo.tools import pycompat
import datetime
import codecs
import base64
import io
from openerp.exceptions import UserError


class ExportMatiereDangereuse(models.Model):
    _name = "export.matiere"

    #### Fields ####
    date_debut = fields.Date(string="Date debut")
    date_fin = fields.Date(string="Date fin")

    file_mat_dange = fields.Char(string='Filename', size=256, readonly=True)
    value_mat_dange = fields.Binary(readonly=True)

    test = fields.Boolean('Test export', help=u"Si coche les lignes exportes ne seront pas marquees comme tel")

    def formatDate(self, dateEN):
        date = dateEN.split('-')
        formatted_date = date[2]+date[1]+date[0][-2:]
        return  formatted_date

    @api.multi
    def export(self, date_debut, date_fin, test, name):


        #### Init des variables #####
        list_row = []

        bl_env = self.env['stock.picking']

        #### preparation du csv ####
        csvfile = io.BytesIO()

        fieldnames = [
           u'SEP', #'S'
           u'DATE',
           u'CODE_TRSP', #01
           u'CODE_PROD', #01
           u'CODE_REM', #01
           u'LIB_REM', #vide
           u'CODE_DEST',
           u'NOM1',
           u'NOM2',#vide
           u'NOM3',#vide
           u'RUE1',
           u'RUE2',
           u'RUE3',#vide
           u'PAYS',
           u'CP',
           u'VILLE',
           u'CONTACT',#vide
           u'TEL',
           u'VIDE1',#vide
           u'REF',
           u'PORT', #'P'
           u'UM',
           u'COLIS',
           u'SUPP_CONS', #vide
           u'TYP_CONS',#vide
           u'POIDS',
           u'UT', #vide
           u'TYPE_UT', #vide
           u'VOL',#vide
           u'CR',#vide
           u'DEV_CR',#vide
           u'VD',#vide
           u'DEV_VD',#vide
           u'VIDE2',#vide
           u'VIDE3',#vide
           u'NAT_MAR',#'MD'/''
           u'INSTR',
           u'REM',#vide
           u'DATE_LIV',#vide
           u'VIDE4',#vide
           u'VIDE5',#vide
           u'TEL_PORT',
           u'MAIL',
        ]

        writer = pycompat.csv_writer(csvfile,delimiter=';')

        writer.writerow(fieldnames)

        bls = bl_env.search([('date','>=', date_debut),('date','<=', date_fin),('exported','=',False),('picking_type_id.code','=','outgoing')])

        for bl in bls:
            liste_line = []
            SEP = 'S'
            date = bl.date
            ref_client = bl.partner_id.parent_id.ref or bl.partner_id.ref
            nom_client = bl.partner_id.display_name or ''
            rue = bl.partner_id.street or ''
            rue2 = bl.partner_id.street2 or ''
            zip = bl.partner_id.zip or ''
            ville = bl.partner_id.city or ''
            pays = bl.partner_id.country_id.code or ''
            tel = bl.partner_id.phone or ''
            mobile = bl.partner_id.mobile or ''
            mail = bl.partner_id.email or ''
            num_bl = bl.name or ''
            um = bl.nb_cartons or ''
            nb_carton = bl.nb_cartons or ''
            weight = bl.weight or ''
            nat_mar = ''
            horaires = bl.partner_id.horaires_livraison or bl.partner_id.parent_id.horaires_livraison

            for line in bl.move_lines:
                if line.product_id.dang:
                    if line.product_id.dang.name != 'Non dangereux' or line.product_id.dang.name != 'Non dangereux  (Inflammable)':
                        nat_mat = 'MD'

            row = [
                SEP,
                date,
                '01',
                '01',
                '01',
                '',
                ref_client,
                nom_client,
                '',
                '',
                rue,
                rue2,
                '',
                pays,
                zip,
                ville,
                '',
                tel,
                '',
                num_bl,
                'P',
                um,
                nb_carton,
                '',
                '',
                weight,
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                nat_mar,
                horaires,
                '',
                '',
                '',
                '',
                mobile,
                mail,
            ]
            writer.writerow(row)


            for line in bl.move_lines :
                if line.product_id.dang:
                    if line.product_id.dang.name == 'Non dangereux' or line.product_id.dang.name == 'Non dangereux  (Inflammable)':
                        continue
                    else:
                        num_dang = line.product_id.dang.num_danger
                        classe = line.product_id.dang.classe
                        ref_art = line.product_id.default_code
                        seg = 'MD'
                        pg = line.product_id.dang.pg
                        desc = line.product_id.display_name + '' +line.product_id.dang.name
                        onu = line.product_id.num_onu
                        poids = line.weight

                        move_row = [
                            seg,
                            onu,
                            desc,
                            pg,
                            '',
                            poids,
                            '',
                            'O'
                        ]

                        writer.writerow(move_row)

                else:
                    continue

            if not test:
                bl.exported = True
        fecvalue = csvfile.getvalue()
        self.write({
            'value_mat_dange':base64.encodestring(fecvalue),
            # 'file_mat_dange':fecvalue,
            'file_mat_dange':name,
        })
        csvfile.close()

    @api.multi
    def action_export(self):
        ##### nom document ######
        date = str(datetime.date.today())
        name = 'Export mat dang %s.csv' % (date)
        self.write({'file_mat_dange': name})


        date_debut = self.date_debut
        date_fin = self.date_fin
        test = self.test

        self.export(date_debut,date_fin, test, name)

        action = {
            'name': 'ecriture_sage',
            'type': 'ir.actions.act_url',
            'url': "web/content/?model=export.matiere&id=" + str(
                self.id) + "&filename_field=file_mat_dange&field=value_mat_dange&download=true&filename=%s.csv" % (name),
            'target': 'new',
        }

        return action




class StockPicking(models.Model):
    _inherit = 'stock.picking'

    exported = fields.Boolean()
