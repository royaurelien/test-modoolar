
from odoo import api, models, fields
from odoo.exceptions import UserError
import sys
import logging
logger = logging.getLogger(__name__)

def logfunc(msg=""):
    caller_funcname = sys._getframe(1).f_code.co_name
    preamble = "[{}] ({})".format(__name__, caller_funcname)

    logger.critical(preamble + " called")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('order_line')
    def onchange_order_line_decond(self):
        """
        trigger des qu'une ligne et changée ou ajoutée ou enlevée,
        sans besoin d'enregistrer le record.
        """
        logfunc()
        # for rec in self:

        self.ensure_one()

        product_obj = self.env['product.product']
        soline_obj = self.env['sale.order.line']
        decond_product = product_obj.search([('name', '=', 'Déconditionnement')])

        if not decond_product:
            msg = """ Il n'existe aucun produit nommé "Déconditionnement" en base.
            Le mécanisme d'ajout de ligne de déconditionnement ne peut pas fonctionner.
            """
            # raise UserError(msg)
            # return {'warning' : {'title': 'Erreur Déconditionnement', 'message': msg }}
            logger.warning(msg)
            return

        # import pudb; pudb.set_trace()
        # si déjà une ligne de déconditionnement, ne rien faire
        line_there = [line for line in self.order_line \
            if line.product_id.id == decond_product.id]

        if line_there:
            logger.critical('already a decond line : setting decond_added for all lines & returning')
            for line in self.order_line:
                line.decond_added = True
            return

        add_decond = False
        for line in self.order_line:
            qty = line.product_uom_qty
            nb_par_colis = line.product_id.nb_par_colis
            logger.critical('nb_par_colis : %s' % nb_par_colis)
            if not nb_par_colis:
                continue
            if ((qty % nb_par_colis) != 0 ) and not line.decond_added  :
                add_decond = True
                break

        # if we decide to add a deconditionnement line,
        # we mark all the present lines as decond_added = True
        # this is for when we remove a line that is a deconditionnement line,
        # it doesnt get re-added instantly...
        if add_decond:
            for line in self.order_line:
                line.decond_added = True
            # self.order_line.write({'decond_added': True})

        if not add_decond:
            return
            # self._ajout_ligne_decond(decond_product)

        """
        ids_list = [x for x in self.order_line]
        logger.critical("ids list : %s" % ids_list)
        return {'values': {'order_line': ids_list }}
        """
        taxes_id = self.partner_id.property_account_position_id.map_tax(decond_product.taxes_id, decond_product, self.partner_id).ids

        values = {
            # 'name': 'déconditionnement',
            'name': decond_product.name,
            'product_id': decond_product.id,
            'price_unit': decond_product.lst_price,
            'product_uom_qty': 1,
            'product_uom': decond_product.uom_id.id,
            'is_decond': True,
            'tax_id':taxes_id,
        }

        # (4, id, 0)
        # line_ids = [(4, x.id, 0) for x in self.order_line]
        line_ids = [x.id for x in self.order_line]

        # https://www.odoo.com/forum/help-1/question/create-new-many2one-records-in-api-onchange-method-2nd-try-70212
        # Jario Llopis answer
        # line_ids.append((0, 0, values))
        nl = soline_obj.new(values)
        line_ids.append(nl.id)
        # line_ids.append((1, nl.id, values))

        """
        order_line = self._fields['order_line'].convert_to_onchange(self._cache['order_line'])
        val_conv =  self._convert_to_cache({'order_line': order_line }, validate=False)
        import pudb; pudb.set_trace()
        self.update(val_conv)
        """
        # self.update({'order_line':line_ids})

        # return
        # import pudb; pudb.set_trace()

        return { 'value': {
            # 'partner_id': 42,
            # 'note': 'I was changed automatically!',
            'order_line': [
                (6, 0, line_ids)
                # line_ids
                # (0, 0, values),
                #(1, 13, {'product_id': decond_product.id, 'product_uom_qty': 10}),
                #(1, 14, {'discount': 15, 'quantity': 34}),
            ]
        } }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    decond_added = fields.Boolean(string="Déconditionnement ajouté")
    is_decond = fields.Boolean(string="Ligne de Deconditionnement")

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)

        res['is_decond'] = self.is_decond

        return res

    """
    @api.onchange('product_id, product_uom_qty')
    def onchange_stuff_line(self):
        logfunc()
    """

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    is_decond = fields.Boolean(string="Ligne de Deconditionnement")
