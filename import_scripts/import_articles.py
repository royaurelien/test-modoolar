#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import logging
import xlrd
import xmlrpclib

logger = logging.getLogger(__name__)

# working with names is better than working with random integers
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

# server_host = "localhost"
server_host = "odoo-domitec.yziact.net"

# server_port = 8071
server_port = 8069

# server_dbname = "domitec_db_one"
server_dbname = "test_one"

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
        print "id : %s" % id
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

        # don't create if family name is empty
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
        """
        dang_id = get_record_id('product.dang', [
            # ['pg', '=', article.pg],
            # ['classe', '=', article.classe],
            # ['num_danger', '=', article.num_danger]
            ['name', '=', article.design]
        ])

        if not dang_id:
            dang_id = create_record(
                'product.dang', {
                    'pg': article.pg,
                    'classe': article.classe,
                    'num_danger': article.num_danger,
                    # 'description': article.design,
                    'name': article.design,
                }
            )

        """
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

        """
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
        """

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
            # 'qty_available': article.stock_phy,
        }

        if not product_tmpl_id:
            product_tmpl_id = create_record('product.template', vals)
        else:
            update_record('product.template', product_tmpl_id, vals)

        # product product
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


# xlrd.xldate.xldate_as_tuple(date_modif, workbook.datemode)
workbook = xlrd.open_workbook('BD_ARTICLES_API.xls')
sheet = workbook.sheet_by_index(0)

curr_row = 2
num_rows = sheet.nrows

importer = ArticleImporter()

while curr_row < num_rows:

    vals = sheet.row_values(curr_row)
    article = Article.from_xls_line(vals)

    print "row_no : %s " % curr_row, article

    importer.import_article(article)

    #if curr_row > 10:
        #break

    curr_row += 1
