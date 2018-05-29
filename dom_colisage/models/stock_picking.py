
from odoo import api, models, fields
import logging
logger = logging.getLogger(__name__)

from .cartons_computer import CartonsComputer, Item

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    nb_cartons = fields.Integer(compute="_compute_nb_cartons", store=True)

    @api.depends('move_lines')
    @api.multi
    def _compute_nb_cartons(self):
        logger.critical('_compute_nb_cartons')

        for rec in self:

            items = []

            for line in rec.move_lines :
                nb_par_colis = line.product_id.nb_par_colis
                nb_delivering = line.quantity_done

                if line.product_id.is_comment == True or 'palette' in line.product_id.name or 'Palette' in line.product_id.name or 'PALETTE' in line.product_id.name:
                    nb_delivering = 0

                items.append(Item(nb_par_colis, nb_delivering))

            rec.nb_cartons = CartonsComputer(items).get_num_cartons()

    @api.multi
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self._compute_nb_cartons()
        return res

    @api.multi
    def do_marquer_comme_fait(self):

        for rec in self:
            for line in rec.move_lines:
                line.quantity_done = line.product_uom_qty

            rec._compute_nb_cartons()

class StockMove(models.Model):
    _inherit = 'stock.move'

    nb_cartons = fields.Integer(compute='_compute_nb_cartons', store=True)

    @api.depends('picking_id.nb_cartons')
    @api.multi
    def _compute_nb_cartons(self):
        items = []

        for rec in self:
            nb_par_colis = rec.product_id.nb_par_colis
            nb_delivering = rec.quantity_done

            if rec.product_id.is_comment == True or 'palette' in rec.product_id.name or 'Palette' in rec.product_id.name or 'PALETTE' in rec.product_id.name:
                nb_delivering = 0

            items.append(Item(nb_par_colis, nb_delivering))

            rec.nb_cartons = CartonsComputer(items).get_num_cartons()

