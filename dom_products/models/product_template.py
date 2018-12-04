# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError, RedirectWarning, except_orm
from odoo.tools import pycompat

"""
famille = fields.Selection([
('01DOC.', '01DOC.'),
('02PUB.', '02PUB.'),
('03MANUT.', '03MANUT.'),
('04ECH.', '04ECH.'),
('ECOFUGEN.', 'ECOFUGEN.'),
('LITHOACCES.', 'LITHOACCES.'),
('LITHOCOTTO.', 'LITHOCOTTO.'),

('LITHOECH.', 'LITHOECH.'),
('LITHOGB.', 'LITHOGB.'),
('LITHOKF.', 'LITHOKF.'),
('LITHOMN.', 'LITHOMN.'),
('LITHOPRIVES.', 'LITHOPRIVES.'),
('LITHOPRO.', 'LITHOPRO.'),
('LITHOUNI.', 'LITHOUNI.'),

('OTTOACCES.', 'OTTOACCES.'),
('OTTOCOLL.', 'OTTOCOLL.'),
('OTTOSEAL.', 'OTTOSEAL.'),
('PAD.', 'PAD.'),
('PROCOVER.', 'PROCOVER.'),
('YPRESTA.', 'YPRESTA.')
], string='Famille')
"""

"""
libelle_famille = fields.Selection([
('Accessoires Lithofin', 'Accessoires Lithofin'),
('Céramique et grès', 'Céramique et grès cérame'),
('Colles', 'Colles'),
('Couverture de chantier', 'Couverture de chantier'),

('Documentation', 'Documentation'),
('Echantillons', 'Echantillons'),
('Echantillons Lithofin', 'Echantillons Lithofin'),

('Labels en anglais', 'Labels en anglais'),
('Labels privés', 'Labels privés'),

('Manutention', 'Manutention'),
('Outils et accessoires Otto', 'Outils et accessoires Otto'),
('Pad', 'Pad'),
('Pierre naturelle', 'Pierre naturelle'),
('Prestations de services', 'Prestations de services'),

('Produits professionnels', 'Prestations professionnels'),
('Publicité', 'Publicité'),
('Silicone', 'Silicone'),
('Stones Eco Fugensand', 'Stones Eco Fugensand'),
('Terre cuite', 'Terre cuite'),
('Universels', 'Universels')
], string=u'Libellé (Famille Article)')
"""

import logging
logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    nb_par_colis = fields.Integer('Nombre par colis')

    eco_dds = fields.Char('Eco DDS')

    # inherited
    weight = fields.Float(string='Poids Brut')
    poids_net = fields.Float(string='Poids Net')

    reliquat_fourn = fields.Integer('Reliquat Fournisseur')
    reliquat_client = fields.Integer('Reliquat Client')
    num_onu = fields.Integer('Num ONU')

    onu_id = fields.Many2one(comodel_name='dom.classification.onu', string="Code ONU")
    family = fields.Many2one(comodel_name='product.family', string="Famille")
    dang = fields.Many2one(comodel_name='product.dang', string=u"Dangerosité")
