
from odoo import api, models, fields
import logging
logger = logging.getLogger(__name__)

from .cartons_computer import CartonsComputer, Item

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    nb_cartons = fields.Integer(string="Nombre de cartons", compute="_compute_nb_cartons", store=True)
    poids_total_brut = fields.Float(string="Poids Total Brut", compute="_compute_poids", store=True)
    poids_total_net = fields.Float(string="Poids Total Net", compute="_compute_poids", store=True)

    @api.depends('order_line')
    def _compute_nb_cartons(self):
        logger.warning('_compute_nb_cartons')

        for rec in self:

            items = []
            for line in rec.order_line:
                if line.is_decond or line.product_id.type != 'product' or line.product_id.name.lower().find('palette') != -1:
                    continue

                nb_par_colis = line.product_id.nb_par_colis
                # nb_delivering = line.quantity_done
                nb_delivering = line.product_uom_qty
                items.append(Item(nb_par_colis, nb_delivering))

            rec.nb_cartons = CartonsComputer(items).get_num_cartons()

    @api.depends('order_line')
    def _compute_poids(self):
        logger.warning('_compute_poids')

        for rec in self:

            poids_brut = 0.0
            poids_net = 0.0
            for line in rec.order_line:
                if line.is_decond or line.product_id.type != 'product':
                    continue
                poids_brut += line.product_id.weight * line.product_uom_qty
                poids_net += line.product_id.poids_net * line.product_uom_qty

            rec.poids_total_brut = poids_brut
            rec.poids_total_net = poids_net
