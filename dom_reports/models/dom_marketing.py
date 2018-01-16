
from odoo import api, models, fields

PARAMS = [
    ("top_message", "domreps_top_message"),
    ("footer_logo_1", "domreps_footer_logo_1"),
    ("footer_logo_2", "domreps_footer_logo_2"),
    ("footer_logo_3", "domreps_footer_logo_3"),
    ("footer_logo_4", "domreps_footer_logo_4"),
    # ("preview_id", "domreps_preview_id"),
    ("prev_id", "domreps_preview_id"),
]

class DomMarketing(models.TransientModel):
    _inherit = 'res.config.settings'
    # _name = 'dom_marketing.config.settings'

    top_message = fields.Binary(string="Message en tête de page")
    footer_logo_1 = fields.Binary(string="Image de pied de page n°1")
    footer_logo_2 = fields.Binary(string="Image de pied de page n°2")
    footer_logo_3 = fields.Binary(string="Image de pied de page n°3")
    footer_logo_4 = fields.Binary(string="Image de pied de page n°4")

    # preview_id = fields.Integer(string="ID du document d'aperçu")
    # preview_id = fields.Many2one("sale.order", "Document d'aperçu")
    prev_id = fields.Many2one("sale.order", "Document d'aperçu")

    # pour pouvoir afficher le même field 2 fois dans une même vue...
    prev_prev_id = fields.Many2one(related='prev_id', store=True)

    @api.model
    def get_values(self):
        res = super(DomMarketing, self).get_values()

        di = {x[0]:self.env['ir.config_parameter'].sudo().get_param(x[1]) for x in PARAMS}
        res.update(di)

        sos = self.env['sale.order'].search([], limit=10)

        try:
            res['prev_id'] = int(res['prev_id'])
        except Exception as e:
            res['prev_id'] = sos[0].id if sos else 1

        return res

    @api.multi
    def set_values(self):
        super(DomMarketing, self).set_values()

        for param in PARAMS:
            self.env['ir.config_parameter'].sudo().set_param(
                param[1], self.__getitem__(param[0])
            )

        self.env['ir.config_parameter'].sudo().set_param('domreps_preview_id',
            self.prev_id.id if self.prev_id else self.env['sale.order'])

        return
