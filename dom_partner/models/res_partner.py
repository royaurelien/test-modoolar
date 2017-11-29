# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class ResPartner(models.Model):
    _inherit = 'res.partner'

    #### RELATIONNEL ####
    famille = fields.Many2one(comodel_name='dom.famille', string='Famille client')
    contact1 = fields.Many2one(comodel_name='res.partner', string='Contact 1')
    contact2 = fields.Many2one(comodel_name='res.partner', string='Contact 2')
    contact3 = fields.Many2one(comodel_name='res.partner', string='Contact 3')

    #### TEXT ####
    code_api = fields.Char(string='Code API')
    horaires_livraison = fields.Text(string="Jours et horaires de livraisons")

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




