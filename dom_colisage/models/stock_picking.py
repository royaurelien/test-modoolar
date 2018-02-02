
from odoo import api, models, fields
import logging
logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    nb_cartons = fields.Integer(compute="_compute_nb_cartons", store=True)

    @api.depends('move_lines')
    def _compute_nb_cartons(self):
        # logger.critical('_compute_nb_cartons')

        for rec in self:

            num_carts = 0
            # remaining_rooms = []

            for line in rec.move_lines :
                nb_par_colis = line.product_id.nb_par_colis
                # nb_delivering = line.product_uom_qty
                # nb_delivering = sum([x.qty_done for x in line.move_line_ids])
                nb_delivering = line.quantity_done

                # logger.critical("nb_delivering : %s" % nb_delivering)
                # logger.critical("nb_par_colis : %s" % nb_par_colis)

                if nb_delivering == 0:
                    continue

                # products with 0 as their nb_par_colis are considered as taking 1 carton
                if nb_par_colis == 0:
                    num_carts += nb_delivering
                    continue

                if nb_par_colis == nb_delivering:
                    num_carts += 1
                    continue

                if nb_delivering <= nb_par_colis:
                    nb = 1
                    # space_remaining = nb_par_colis - nb_delivering
                else:
                    nb = nb_delivering // nb_par_colis
                    reste = nb_delivering % nb_par_colis
                    # space_remaining = nb_par_colis - reste
                    if reste:
                        nb += 1

                num_carts += nb

                # room remaining in the last used carton
                # remaining_room = 1 - (float(remains) / float(nb_par_colis))
                # remaining_rooms.append(remaining_room)

            rec.nb_cartons = num_carts

    @api.multi
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self._compute_nb_cartons()
        return res
