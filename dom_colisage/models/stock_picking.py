
from odoo import api, models, fields
import logging
logger = logging.getLogger(__name__)

from .cartons_computer import CartonsComputer, Item

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    nb_cartons = fields.Integer(compute="_compute_nb_cartons", store=True)

    @api.depends('move_lines')
    def _compute_nb_cartons(self):
        # logger.critical('_compute_nb_cartons')

        for rec in self:

            items = []
            for line in rec.move_lines :
                nb_par_colis = line.product_id.nb_par_colis
                nb_delivering = line.quantity_done
                items.append(Item(nb_par_colis, nb_delivering))

            rec.nb_cartons = CartonsComputer(items).get_num_cartons()

    @api.multi
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self._compute_nb_cartons()
        return res
