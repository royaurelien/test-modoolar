# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, timedelta
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    ##### Numerique #####
    effectif = fields.Integer(string=u"Effectif de l'entreprise")
    chiffre_affaire = fields.Integer(string=u"CA l'entreprise")
    periode = fields.Integer(string='periode', help=u'Temps en jours estimé après lequel un contact est négligé')
    revenu_mensuel = fields.Float(string=u"Revenu mensuel estimé")
    marge_estimee = fields.Float(string=u'Marge Estimée')

    ##### DATE ####
    # annee_effectif = fields.Date(string=u"Année de l'effectif")
    # annee_chiffre_affaire = fields.Date(string=u"Année du CA")
    dernier_devis = fields.Date(string=u"Date dernier devis")
    date_neglected  = fields.Date(string='Date neglected', compute='compute_neglected', store=True)


    ##### SELECTION ####
    type_rel = fields.Selection([
        # ('prospect', 'Prospect'),
        ('client', 'Client'),
        ('client_old', 'Client existant'),
        # ('concurrent', 'Concurrent'),
        # ('partenaire', 'Partenaire'),
        # ('com', 'Presse/Communication'),
    ],string=u"Type de relation")
    service_informatique = fields.Selection([
        ('interne', 'Interne'),
        ('sous-traitee', u'sous-traitée'),
    ], sting=u"Service informatique")
    role_interlocuteur =  fields.Selection([
        ('decisionnaire',u'Décisionnaire'),
        ('prescriteur_int_direction', u'Prescripteur interne Direction'),
        ('prescriteur_int',u'Prescripteur interne Hors Direction'),
        ('prescripteur_ext', u'Prescripteur externe')
    ], string=u"Rôle de l’interlocuteur")

    annee_effectif = fields.Selection([(num, str(num)) for num in range((datetime.now().year)+20,1999, -1)],string=u"Année de l'effectif")
    annee_chiffre_affaire = fields.Selection([(num, str(num)) for num in range((datetime.now().year)+20,1999, -1)],string=u"Année du CA")

    ##### RELATIONNEL ####
    ape_id = fields.Many2one('res.partner.ape', string='APE', help="If the partner is a French company, enter its official "
             "main activity in this field. The APE is chosen among the "
             "NAF nomenclature.")
    hidden_stage = fields.Char('hidden_stage_name', related='stage_id.hidden_name')


    @api.depends('dernier_devis', 'periode')
    @api.multi
    def compute_neglected(self):
        for lead in self:
            periode = lead.periode

            #cas ou la configuration serait passee a l' as
            if not periode:
                periode=60

            # if self.dernier_devis:
                # dernier_devis = datetime.strptime(self.dernier_devis, "%Y-%m-%d")

            date_neglected = date.today()- timedelta(days=periode)
            lead.date_neglected = date.strftime(date_neglected, '%Y-%m-%d')


    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(CrmLead, self)._onchange_partner_id()
        if self.partner_id.ape_id:
            self.ape_id = self.partner_id.ape_id.id

        return res

    @api.onchange('dernier_devis')
    def onchange_dernier_devis(self):
        values = self.onchange_dernier_devis_values(self.dernier_devis)
        self.update(values)

        if self.partner_id:
            self.partner_id.change_date(self.dernier_devis)


    def onchange_dernier_devis_values(self,date):
        values = {}
        if date :
            values['dernier_devis'] = date

        return values


    def _lead_create_contact(self, cr, uid, lead, name, is_company, parent_id=False, context=None):
        partner_env = self.pool.get('res.partner')
        res = super(CrmLead, self)._lead_create_contact(cr, uid, lead, name, is_company, parent_id, context)
        partner_obj = partner_env.browse(cr, uid, res, context)
        vals = {}

        if is_company:
            vals['effectif'] = lead.effectif
            vals['annee_effectif'] = lead.annee_effectif
            vals['chiffre_affaire'] = lead.chiffre_affaire
            vals['annee_chiffre_affaire'] = lead.annee_chiffre_affaire
            vals['type_rel'] = lead.type_rel
            vals['ape_id'] = lead.ape_id.id
            vals['service_informatique'] = lead.service_informatique

            partner_obj.write(vals)

        return res



# class CrmconfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'
#     _name = 'crm.config.settings'
#
#
#     default_periode = fields.Integer(default_model='crm.lead')
#     default_date_neglected = fields.Date(default_model='crm.lead', default='1942-04-01')
#
#     @api.model
#     def get_default_periode_values(self, fields):
#         return {'periode':60}
#
