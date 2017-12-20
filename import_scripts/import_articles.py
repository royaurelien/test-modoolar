#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import argparse

import xlrd
import xmlrpclib

logger = logging.getLogger(__name__)

# argparse
parser = argparse.ArgumentParser(description='Articles Import Script')
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")

args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

# working with names is better than working with random integers
# pour NouvelleBaseArticles.xlsx
names_to_ints = {
    'code': 0, # a
    'famille': 1, # b
    'libelle': 2, # c
    'unite vente': 3, # d
    'nombre par colis': 4, # e
    'poids brut': 5, # f
    'stock physique': 6, # g
    'date modification': 7, # h
    'dernier prix': 8, # i
    'prix base ht': 9, # j
    'libelle (famille article)': 10, # k
    'num ONU': 11, # L
    'categorie': 12, # m
    'designation': 13, # n
    'PG': 14, # o
    'classe': 15, # p
    'num danger': 16, # q
    'code barre': 17, # r

    # 'reliquat fournisseur': 11, # l
    # 'reliquat client': 12, #
    # 'categorie': 14,
    # 'designation': 15,
    # 'PG': 16,
    # 'classe': 17,
    # 'num danger': 18,
    # 'code barre': 19,
}

# {{{ odoo xmlrpc stuff

server_host = "localhost"
# server_host = "odoo-domitec.yziact.net"

server_port = 8071
# server_port = 8069

# server_dbname = "domitec_db_one"
# server_dbname = "test_one"
server_dbname = "based_one"

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

    try:
        res = models.execute_kw(server_dbname, server_uid, server_pwd,
            model_name, 'create', [data_dict])

    except Exception as e:
        print "erreur lors de la creation de %s" % model_name
        print "avec les valeurs : %s" % data_dict
        import pudb; pudb.set_trace()
        raise

    return res

def update_record(model_name, rec_id, data_dict):

    try:
        res = models.execute_kw(server_dbname, server_uid, server_pwd,
            model_name, 'write', [[rec_id], data_dict])

    except Exception as e:
        print "erreur lors de la l'update de %s" % model_name
        print "id : %s" % rec_id
        print "avec les valeurs : %s" % data_dict
        import pudb; pudb.set_trace()
        raise

    return res

def get_record_id(model_name, domain):


    try:
        res = models.execute_kw(server_dbname, server_uid, server_pwd,
            model_name, 'search', [domain])
    except Exception as e:
        print "le model %s n'existe pas" % model_name
        raise

    return res[0] if res else False

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
        self.nb_par_colis = nb_par_colis
        self.poids_brut = poids_brut
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
        self.pg = pg
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
        reliq_fourn = None # get(xl, 'reliquat fournisseur')
        reliq_client = None # get(xl, 'reliquat client')
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

    def to_dict(self):
        """
        returns the article as a dict, ready to be given to Odoo,
        with the right field names
        """
        pass


class ArticleImporter(object):

    def __init__(self):

        self.uom_categ_id_unit = get_record_id('product.uom.categ', [
            ['name', 'ilike', 'Unit'],
        ])

        self.uom_categ_id_volume = get_record_id('product.uom.categ', [
            ['name', 'ilike', 'Volume'],
        ])

        self.uom_id_unit = get_record_id('product.uom', [
            ['name', 'ilike', 'unit'],
        ])

        if not self.uom_id_unit:
            raise Exception("ID of uom_id unit not found")

        logger.debug('self.uom_id_unit : %s' % self.uom_id_unit)

        if (not self.uom_categ_id_unit) or (not self.uom_categ_id_volume):
            raise Exception(u"Pas de catégorie d'unité Unité ou Volume")

    def figure_uom_id(self, uname):

        unit_units = {
            'Unit': 'Unit',
            'unit': 'unit',
            u'Unité': u'Unité',
            'U': 'U',
            'KIT': 'KIT',
            '1CART': '1CART',
        }

        volume_units = {
            '0.100': '0.100L',
            '0.150': '0.150L',
            '0.200': '0.200L',
            '0.250': '0.250L',
            '0.300': '0.300L',
            '0.310': '0.310L',
            '0.500': '0.500L',
            '1L': '1L',
            '2.5': '2.5L',
            '5': '5L',
            '2.5L': '2.5L',
            '5L': '5L',
            '10L': '10L',
            '30L': '30L',
        }

        # always use unit...
        return self.uom_id_unit

        uom_categ_id = None
        if uname in unit_units:
            uom_categ_id = self.uom_categ_id_unit
            uname = unit_units[uname]
        elif uname in volume_units:
            uom_categ_id = self.uom_categ_id_volume
            uname = volume_units[uname]

        if not uom_categ_id:
            import pudb; pudb.set_trace()
            raise Exception("Could not figure out uom_categ_id")

        uom_id = get_record_id('product.uom', [
            ['name', '=', uname],
        ])

        if not uom_id:
            uom_id = create_record(
                'product.uom', {
                    'name': uname,
                    'category_id': uom_categ_id,
                }
            )

        return uom_id

    def figure_fam_id(self, article):

        # don't create if family name is empty
        if article.fam == "":
            return 0

        fam_id = get_record_id('product.family', [
            ['name', '=', article.fam],
        ])

        if not fam_id:
            fam_id = create_record(
                'product.family', {
                    'name': article.fam,
                    'libelle': article.lib_fam,
                }
            )

        return fam_id

    def figure_stuff_out(self, model_name, article, name_value, data_dict):

        # don't create if name is empty
        if name_value == "":
            return 0

        record_id = get_record_id(model_name, [
            ['name', '=', name_value],
        ])

        if not record_id:
            record_id = create_record(model_name, data_dict)

        return record_id

    def import_article(self, article):

        # dangerosity
        dang_id = self.figure_stuff_out('product.dang', article,
        article.design, {
            'pg': article.pg,
            'classe': article.classe,
            'num_danger': article.num_danger,
            'name': article.design,
        })

        # category
        categ_id = get_record_id('product.category', [
            ['name', '=', article.categ],
        ])

        if not categ_id:
            categ_id = create_record(
                'product.category', {
                    'name': article.categ,
                }
            )

        # family
        fam_id = self.figure_fam_id(article)

        # uom
        uom_id = self.figure_uom_id(article.unite)

        # product template
        product_tmpl_id = get_record_id('product.template', [
            ['name', '=', article.lib],
        ])

        vals = {
            'type': 'product',

            'uom_id': uom_id,
            'uom_po_id': uom_id,

            'sale_ok': True,
            'website_published': False,
            'taxes_id': [(6, 0, [1])],

            'name': article.lib,
            'default_code': article.code,
            'price': article.prix_base_ht,

            'standard_price': article.dernier_prix,
            'categ_id': categ_id,

            'family': fam_id,
            'dang': dang_id,

            'nb_par_colis': article.nb_par_colis,
            'poids_brut': article.poids_brut,
            # 'qty_available': article.stock_phy,
        }

        if product_tmpl_id:
            update_record('product.template', product_tmpl_id, vals)
        else:
            product_tmpl_id = create_record('product.template', vals)

        # After the template is created, search the product, affect the barcode, you're done..
        vals = {
            'barcode': article.code_barre,
        }

        product_id = get_record_id('product.product', [
            ['name', '=', article.lib],
        ])

        if product_id and article.code_barre:
            # si le code barre existe déjà en db,
            # ceci va échouer
            try:
                update_record('product.product', product_id, vals)
            except Exception as e:
                # osef
                pass
        else:
            print "product_id not found..."

        logger.info("article importé... ref: {}, barcode: {}".format(
            article.code, article.code_barre
        ))
        # product product
        """
        product_id = get_record_id('product.product', [
            #['name', '=', article.lib],
            ['barcode', '=', article.code_barre],
        ])

        vals = {
            'product_tmpl_id': product_tmpl_id,
            'barcode': article.code_barre,
            # 'qty_available': article.stock_phy,
        }
        if not product_id:
            product_id = create_record('product.product', vals)
        else:
            update_record('product.product', product_id, vals)
        """


# xlrd.xldate.xldate_as_tuple(date_modif, workbook.datemode)


class ArticlesReader(object):

    @staticmethod
    def read_from_xls(filename):
        """
        reads articles from file
        returns a list of Articles
        """

        workbook = xlrd.open_workbook(filename)
        sheet = workbook.sheet_by_index(0)

        curr_row = 2
        num_rows = sheet.nrows

        art_list = []
        while curr_row < num_rows:

            vals = sheet.row_values(curr_row)
            article = Article.from_xls_line(vals)

            art_list.append(article)

            # print "row_no : %s " % curr_row, article

            curr_row += 1
        return art_list



# articles = ArticlesReader.read_from_xls('BD_ARTICLES_API.xls')
articles = ArticlesReader.read_from_xls('NouvelleBaseArticles.xlsx')

# for i, article in enumerate(articles):
    # print i+1, article

importer = ArticleImporter()

for article in articles:
    importer.import_article(article)
