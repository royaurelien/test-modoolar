# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from datetime import datetime

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
    contact1 = fields.Many2one(comodel_name='res.partner', string=u'Gérant', domain="[('id', 'in', 'child_ids)]")
    contact2 = fields.Many2one(comodel_name='res.partner', string=u'Achat', domain="[('id', 'in', 'child_ids)]")
    contact3 = fields.Many2one(comodel_name='res.partner', string=u'Comptabilité', domain="[('id', 'in', 'child_ids)]")
    transporteur = fields.Many2one(comodel_name='dom.transporteur', string='Transporteur')
    child_ids_2 = fields.One2many('res.partner', 'parent_id', string='Filiale',
                                  domain=[('active', '=', True), ('company_type', '=', 'company')],
                                  default=get_child_ids)
    child_ids = fields.One2many(domain=[('active', '=', True), ('company_type', '=', 'person')])
    presentoir_id = fields.Many2one(comodel_name='dom.presentoir', string=u'Présentoir')

    #### TEXT ####
    code_api = fields.Char(string='Code API')
    horaires_livraison = fields.Text(string="Jours et horaires de livraisons")
    fax = fields.Char(string="fax")

    #### NUMERIQUE ####
    ca_12 = fields.Float(compute='compute_ca_year', string='CA 12 mois')
    taux_commission = fields.Float(string='Commission (%)')
    url_bfa = fields.Char(string='URL BFA')


    #### BOOLEAN ####
    paie_livraison = fields.Boolean(string='Paiement avant livraison')
    fac_mail = fields.Boolean(string='Facture par mail')
    bfa = fields.Boolean(string="BFA")
    plv = fields.Boolean(string=u"Publicité sur lieu de vente")
    presentoir = fields.Boolean(string=u"Présentoir")

    #### DATE ####
    plv_pdt = fields.Date(string=u'PLV plan de travail')
    plv_p_int = fields.Date(string=u'PLV pierre intérieure')
    plv_p_ext = fields.Date(string=u'PLV pierre extérieure')
    plv_carrelage = fields.Date(string=u'PLV carrelage')

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

    #### COMPUTE ####
    @api.multi
    def compute_ca_year(self):
        date = datetime.today()
        year = date.year

        account_invoice_report = self.env['account.invoice.report']
        if not self.ids:
            self.total_invoiced = 0.0
            return True

        user_currency_id = self.env.user.company_id.currency_id.id
        all_partners_and_children = {}
        all_partner_ids = []
        for partner in self:
            # price_total is in the company currency
            all_partners_and_children[partner] = self.with_context(active_test=False).search(
                [('id', 'child_of', partner.id)]).ids
            all_partner_ids += all_partners_and_children[partner]

        # searching account.invoice.report via the orm is comparatively expensive
        # (generates queries "id in []" forcing to build the full table).
        # In simple cases where all invoices are in the same currency than the user's company
        # access directly these elements

        # generate where clause to include multicompany rules
        where_query = account_invoice_report._where_calc([
            ('partner_id', 'in', all_partner_ids), ('state', 'not in', ['draft', 'cancel']),
            ('type', 'in', ('out_invoice', 'out_refund')),('date','ilike','%'+str(year)+'%')
        ])
        account_invoice_report._apply_ir_rules(where_query, 'read')
        from_clause, where_clause, where_clause_params = where_query.get_sql()

        # price_total is in the company currency
        query = """
                      SELECT SUM(price_total) as total, partner_id
                        FROM account_invoice_report account_invoice_report
                       WHERE %s
                       GROUP BY partner_id
                    """ % where_clause
        self.env.cr.execute(query, where_clause_params)
        price_totals = self.env.cr.dictfetchall()
        for partner, child_ids in all_partners_and_children.items():
            partner.ca_12 = sum(
                price['total'] for price in price_totals if price['partner_id'] in child_ids)
