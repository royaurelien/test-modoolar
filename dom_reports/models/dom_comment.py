
from odoo import api, models, fields
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class DomComments(models.Model):
    _name = 'dom.comment'

    code = fields.Char(string="Code du commentaire")
    value = fields.Html(string="Valeur du commentaire")

    def name_get(self):

        res = []

        for rec in self:
            stripped_value = strip_tags(rec.value)
            res.append((rec.id, (rec.code + ' - ' if rec.code else '') + stripped_value))

        return res
