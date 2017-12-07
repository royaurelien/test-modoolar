# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ##### Numerique #####
    effectif = fields.Integer(string=u"Effectif de l'entreprise")
    chiffre_affaire = fields.Integer(string=u"CA l'entreprise")

    ##### DATE ####
    # annee_effectif = fields.Date(string=u"Année de l'effectif")
    # annee_chiffre_affaire = fields.Date(string=u"Année du CA")
    dernier_devis = fields.Date(string=u"Date dernier devis")

    ##### SELECTION ####
    type_rel = fields.Selection([
        ('prospect', 'Prospect'),
        ('client', 'Client'),
        ('client_old', 'Ancien Client'),
        ('client_ind', 'Client Indirect'),
        ('group', 'Groupe'),
        ('concurrent', 'Concurrent'),
        ('partner', 'Partenaire'),
        ('com', 'Presse/Communication'),
    ],string=u"Type de relation")
    service_informatique = fields.Selection([
        ('interne', 'Interne'),
        ('sous-traitee', u'sous-traitée'),
    ], sting=u"Service informatique")
    annee_effectif = fields.Selection([(num, str(num)) for num in range((datetime.now().year) + 20, 1999, -1)],
                                      string=u"Année de l'effectif")
    annee_chiffre_affaire = fields.Selection([(num, str(num)) for num in range((datetime.now().year) + 20, 1999, -1)],
                                             string=u"Année du CA")

    ##### RELATIONNEL ####
    tag_ids =  fields.Many2many('crm.lead.tag', 'crm_partner_tag_rel', 'partner_id', 'tag_id', u'Intérêts')

    def change_date(self, date):
        dernier_devis = self.dernier_devis

        if not dernier_devis:
            return self.write({'dernier_devis':date})

        dernier_devis = datetime.strptime(self.dernier_devis, '%Y-%m-%d').date()

        if date > dernier_devis:
            return self.write({'dernier_devis': date})

        return True

    @api.onchange('type_rel')
    def onchange_type_rel(self):
        values = self.onchange_type_rel_values(self.type_rel)

        return self.update(values)


    def onchange_type_rel_values(self, type_rel):
        vals = {}
        is_client = self.customer

        if type_rel == 'prospect' or type_rel == 'client_old':
            is_client = False

        elif type_rel == 'client':
            is_client = True

        vals['customer'] = is_client
        return vals


