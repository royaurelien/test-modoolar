# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def get_child_ids(self):
        vals = []

        for child in self.child_ids :
            if child.company_type == 'company':
                vals.append(child)

        return vals

    #### RELATIONNEL ####
    famille = fields.Many2one(comodel_name='dom.famille', string='Famille client')
    contact1 = fields.Many2one(comodel_name='res.partner', string='Contact 1')
    contact2 = fields.Many2one(comodel_name='res.partner', string='Contact 2')
    contact3 = fields.Many2one(comodel_name='res.partner', string='Contact 3')
    transporteur = fields.Many2one(comodel_name='dom.transporteur', string='Transporteur')
    child_ids_2 = fields.One2many('res.partner', 'parent_id', string='Filiale',
                                  domain=[('active', '=', True), ('company_type', '=', 'company')],
                                  default=get_child_ids)
    #### TEXT ####
    code_api = fields.Char(string='Code API')
    horaires_livraison = fields.Text(string="Jours et horaires de livraisons")
    fax = fields.Char(string="fax")

    #### NUMERIQUE ####
    ca_12 = fields.Integer(string='CA 12 mois')
    taux_commission = fields.Float(string='Commission (%)')
    url_bfa = fields.Char(string='URL BFA')


    #### BOOLEAN ####
    paie_livraison = fields.Boolean(string='Paiement avant livraison')
    fac_mail = fields.Boolean(string='Facture par mail')
    bfa = fields.Boolean(string="BFA")
    plv = fields.Boolean(string=u"Publicité sur lieu de vente")
    presentoir = fields.Boolean(string=u"Présentoir")


    #### SELECTION ####
    freq_contact = fields.Selection([
        ('1','1 mois'),
        ('3','3 mois'),
        ('6','6 mois'),
        ('12','12 mois')
    ], string=u"Fréquence de contact")
    company_type = fields.Selection(store=True)

    #### ONCHANGE ####
    @api.onchange('famille')
    def onchange_famille(self):
        vals = self.onchange_famille_values(self.famille)
        self.update(vals)


    def onchange_famille_values(self, famille):
        values = {}
        if famille :
            if famille.property_product_pricelist:
                values['property_product_pricelist'] = famille.property_product_pricelist.id

        return values




