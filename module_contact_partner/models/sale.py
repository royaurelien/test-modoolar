from openerp import models, fields, api, exceptions, _
from datetime import timedelta


class Partner(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(Partner, self).onchange_partner_id()
        
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment term
        - Invoice address
        - Delivery address
        """
        partner_env = self.env['res.partner']

        print "OUR ONCHANGE_PARTNER_ID"

        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'payment_term_id': False,
                'fiscal_position_id': False,
            })
            return

        shipping_addr = partner_env.search([('parent_id', '=', self.partner_id.id), ('type', '=', 'delivery')])
        invoicing_addr = partner_env.search([('parent_id', '=', self.partner_id.id), ('type', '=', 'invoice')])
        ship = ''
        inv = ''
        if shipping_addr:
            ship = shipping_addr.id

        if invoicing_addr:
            inv = invoicing_addr.id

        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': inv or self.partner_id.id,
            'partner_shipping_id': ship or self.partner_id.id,
            'note': self.with_context(lang=self.partner_id.lang).env.user.company_id.sale_note,
        }

        if self.partner_id.user_id:
            values['user_id'] = self.partner_id.user_id.id
        if self.partner_id.team_id:
            values['team_id'] = self.partner_id.team_id.id
        self.update(values)
