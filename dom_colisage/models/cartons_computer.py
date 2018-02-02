
class Item(object):

    def __init__(self, num_per_carton, nb_delivering):
        self.num_per_carton = num_per_carton
        self.nb_delivering = nb_delivering

class CartonsComputer(object):

    def __init__(self, items_list):
        self.items = items_list

    def get_num_cartons(self):

        num_carts = 0

        for item in self.items:
            # nb_par_colis = line.product_id.nb_par_colis
            nb_par_colis = item.num_per_carton
            # nb_delivering = line.product_uom_qty
            # nb_delivering = sum([x.qty_done for x in line.move_line_ids])
            nb_delivering = item.nb_delivering

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

        return num_carts
