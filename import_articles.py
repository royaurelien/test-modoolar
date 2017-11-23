#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import logging
import xlrd
import xmlrpclib

logger = logging.getLogger(__name__)

names_to_ints = {
    'code': 0,
    'famille': 1,
    'libelle': 2,
    'unite vente': 3,
    'nombre par colis': 4,
    'poids brut': 5,
    'stock physique': 6,
    'date modification': 7,
    'dernier prix': 8,
    'prix base ht': 9,
    'libelle (famille article)': 10,
    'reliquat fournisseur': 11,
    'reliquat client': 12,
    'num ONU': 13,
    'categorie': 14,
    'designation': 15,
    'PG': 16,
    'classe': 17,
    'num danger': 18,
    'code barre': 19,
}

# {{{ odoo xmlrpc stuff
server_host = "localhost"
server_port = 8071
server_dbname = "domitec_db_one"
server_username = 'admin'
server_pwd = 'X200yziact'

server_url = 'http://' + server_host + ':' + str(server_port)

sock_common = xmlrpclib.ServerProxy(server_url + '/xmlrpc/2/common')

models = xmlrpclib.ServerProxy(server_url + '/xmlrpc/2/object')

server_uid = 0
try:
    server_uid = sock_common.login(server_dbname, server_username, server_pwd)
except Exception as e:
    logger.critical('Odoo connection failed')

def create_record(model_name, data_dict):

    res = models.execute_kw(server_dbname, server_uid, server_pwd,
        model_name, 'create', data_dict)

    return res

def get_record_id(model_name, domain):

    res = models.execute_kw(server_dbname, server_uid, server_pwd,
        model_name, 'search', [domain])

    return res

def record_with_name_exists(model_name, name):

    res = get_record_id(model_name, [['name','=',name]])

    return res[0] if res else False

def record_with_x_exists(model_name, x, x_value):

    res = get_record_id(model_name, [[x,'=',x_value]])

    return res[0] if res else False

def create_or_get(model_name, data_dict, name):
    """
    if a record with the same name exists, get the id, return the id.

    if a record doesn't exist, create it, return the id
    """

    rec_id = 0
    existing_rec_id = record_with_name_exists(model_name, name)
    if existing_rec_id:
        rec_id = existing_rec_id
    else:
        rec_id = create_record(model_name, data_dict)

    return rec_id

# }}}

class Article(object):

    def __init__(self, code, famille, libelle, unite_vente, nb_par_colis,
            poids_brut, stock_phy, date_modif, dernier_prix, prix_base_ht,
            libelle_fam, reliq_fourn, reliq_client, num_onu, categ, design,
            pg, classe, num_danger, code_barre):
        """
        line is a LIST OF XLRD.sheet.CELL class
        type(line[0]) = xlrd.sheet.cell
        """
        # self.orig_line = line
        # self.line = line
        # self.line_arr = line.split(";")
        self.code = code
        self.fam = famille
        self.lib = libelle
        self.unite = unite_vente
        self.nb_par_colis = poids_brut
        self.stock_phy = stock_phy
        self.date_modif = date_modif
        self.dernier_prix = dernier_prix
        self.prix_base_ht = prix_base_ht
        self.lib_fam = libelle_fam
        self.reliq_fourn = reliq_fourn
        self.reliq_client = reliq_client
        self.num_onu = num_onu
        self.categ = categ
        self.design = design
        self.classe = classe
        self.num_danger = num_danger
        self.code_barre = code_barre

    def get(self, name):
        try:
            # return self.line_arr[names_to_ints[name]]
            # return self.line[names_to_ints[name]]
            return self.line[names_to_ints[name]]
        except IndexError:
            return "no value for %s" % name

    def import_line(self):
        """ actually send the line to Odoo """

        res = models.execute_kw(server_dbname, server_uid, server_pwd,
            'product.template', 'create', lines)

        res = create_model('product_template')

    @classmethod
    def from_xls_line(cls, xl):

        def get(line, name):
            return line[names_to_ints[name]]

        code = get(xl, 'code')
        fam = get(xl, 'famille')
        lib = get(xl, 'libelle')
        unite = get(xl, 'unite vente')
        nb_par_colis = get(xl, 'nombre par colis')
        poids_brut = get(xl, 'poids brut')
        stock_phy = get(xl, 'stock physique')
        date_modif = get(xl, 'date modification')
        dernier_prix = get(xl, 'dernier prix')
        prix_base_ht = get(xl, 'prix base ht')
        lib_fam = get(xl, 'libelle (famille article)')
        reliq_fourn = get(xl, 'reliquat fournisseur')
        reliq_client = get(xl, 'reliquat client')
        num_onu = get(xl, 'num ONU')
        categ = get(xl, 'categorie')
        design = get(xl, 'designation')
        pg = get(xl, 'PG')
        classe = get(xl, 'classe')
        num_danger = get(xl, 'num danger')
        code_barre = get(xl, 'code barre')

        return cls(code, fam, lib, unite, nb_par_colis, poids_brut, stock_phy,
            date_modif, dernier_prix, prix_base_ht, lib_fam, reliq_fourn,
            reliq_client, num_onu, categ, design, pg, classe, num_danger,
            code_barre)

    def __str__(self):
        # li = [self.code, self.fam, self.lib, self.unite, self.dernier_prix,
              #self.stock_phy, self.prix_base_ht, self.code_barre]

        # return str(li)
        return str(self.__dict__)


# xlrd.xldate.xldate_as_tuple(date_modif, workbook.datemode)
workbook = xlrd.open_workbook('BD_ARTICLES_API.xls')
sheet = workbook.sheet_by_index(0)

curr_row = 2
num_rows = sheet.nrows

while curr_row < num_rows:

    # line = CsvLine(sheet.row(curr_row))

    vals = sheet.row_values(curr_row)
    article = Article.from_xls_line(vals)
    # print line.get('code')
    # print line.get('dernier prix')
    # print line.get('prix base ht')

    print "row_no : %s " % curr_row, article, article.dernier_prix

    curr_row += 1
