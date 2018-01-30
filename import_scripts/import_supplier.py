#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmlrpclib
import csv
import sys
from datetime import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

def set_connexion_doodoo():
    global pwd
    global dbname
    global sock_common
    global uid
    global sock

    # Connexion Odoo
    hostname = '127.0.0.1'
    port = '8071'
    username = "admin"
    pwd = "X200yziact"
    # dbname = "DOM_12_01"
    # dbname = "based_as_cs"
    dbname = "domitec_conds"

    sock_common = xmlrpclib.ServerProxy("http://" + hostname + ":" + port + "/xmlrpc/2/common")
    uid = sock_common.login(dbname, username, pwd)
    sock = xmlrpclib.ServerProxy("http://" + hostname + ":" + port + "/xmlrpc/2/object")


def search_reg(code_regl):
    cond_reg_id = False

    if code_regl:
        reg = sock.execute(dbname, uid, pwd, 'account.payment.term', 'search', ([('name','=',code_regl)]))

        if reg:
            print(reg)
            cond_reg_id = reg[0]


    return cond_reg_id

def search_fam(fam_name):
    fam_id = False
    print fam_name

    if fam_name:
        fam = sock.execute(dbname, uid, pwd, 'res.country', 'search_read', ([('name', '=', fam_name)]),('id'))
        if fam :
            fam_id=fam[0]['id']


    return fam_id

def search_country(country):

    name = False
    if country in ['f', 'fr', 'Fr', 'FR', 'FRANCE', 'France', 'france']:
        name = 'France'
    elif country in ['Allemagne']:
        name = 'Germany'
    elif country in ['The Netherlands', 'HOLLAND', 'hollande']:
        name = 'Netherlands'
    elif country in ['Italie', 'ITALIA']:
        # name = 'Italie'
        name = 'Italy'
    elif country in ['belgique']:
        name = 'Belgium'

    if not name:
        print ("erreur : pays non défini : %s" % country)
        return False

    country_id = False

    if name:
        co = sock.execute(dbname, uid, pwd, 'res.country', 'search_read', ([('name', '=', name)]) )
        if co :
            country_id = co[0]['id']

    print u"%s = %s " % (country, name)
    print u"country_id = %s" % country_id

    if not country_id:
        raise("Country not found : %s" % name)
    # import pudb; pudb.set_trace()

    return country_id

set_connexion_doodoo()
fich_ = open('fournisseurs_V2import_gcsv.csv', 'rb')

csvreader = csv.reader(fich_, delimiter=';')

tot = 0
i = 1

type_rel = sock.execute(dbname, uid, pwd, 'crm_yzi.type_rel','search_read', ([('name', '=', 'Fournisseur')]), ('id'))

type_rel_id = type_rel[0]['id']

# print "sys exitting"
# sys.exit()

def get_partner_id(domain):

    try:
        res = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'search', [domain])
    except Exception as e:
        print "le model %s n'existe pas" % model_name
        raise

    return res[0] if res else False

def create_or_update_supplier(partner_dict):

    id = 0
    partner_id = get_partner_id([ ['name', '=', partner_dict['name']], ['supplier', '=', True] ])
    print "partner_id : %s" % partner_id
    print "partner_dict : %s" % partner_dict
    if partner_id:
        id = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'write', [[partner_id], partner_dict])
        id = partner_id
        print "update"
    else :
        id = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'create', [partner_dict])
        print "create"

    # import pudb; pudb.set_trace()
    return id

def create_or_update_contact(contact_dict):

    id = 0
    partner_id = get_partner_id([
        ['name', '=', contact_dict['name']],
        ['type', '=', contact_dict['type']],
        ['parent_id', '=', contact_dict['parent_id']],
    ])
    print "partner_id : %s" % partner_id
    print "partner_dict : %s" % partner_dict
    if partner_id:
        id = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'write', [[partner_id], partner_dict])
        id = partner_id
        print "update"
    else :
        id = sock.execute_kw(dbname, uid, pwd, 'res.partner', 'create', [partner_dict])
        print "create"

    # import pudb; pudb.set_trace()
    return id

for row in csvreader:
    print i
    print row[0]
    if i <= 3 :
        i += 1
        continue

    # champ pour le Compte
    company_type = 'company'
    trust = 'normal'
    customer = False
    supplier = True
    is_company = True

    name = row[0]
    phone = row[1]
    cod_reg = row[4]
    famille_raw = row[5].strip()
    street = row[7]
    city = row[8]
    zip = row[9].strip()
    country = row[10]
    website = row[12]
    famille = famille_raw[0].upper()+famille_raw[1:].lower() if famille_raw else ''

    cond_reg_id = search_reg(cod_reg)
    famille_id = search_fam(famille)
    country_id = search_country(country)

    if row[11]:
        phone += ';'+row[11]

    tot += 1

    partner_dict = {
        'company_type': company_type,
        'trust': trust,
        'customer': customer,
        'supplier': supplier,
        'is_company': is_company,
        'name': name,
        'phone': phone,
        'street': street,
        'city': city,
        'zip': zip,
        'country_id': country_id,
        'website': website,
        'famille_fournisseur':famille_id,
        'property_supplier_payment_term_id':cond_reg_id,
        'type_rel':type_rel_id,
    }

    compte = 0
    compte = create_or_update_supplier(partner_dict)

    if row[3]:
        type = 'contact'
        parent_id_inv = compte
        name_cont = row[3]
        mobile = row[14]

        contact_dict = {
            'type': type,
            'parent_id': parent_id_inv,
            'mobile': mobile,
            'name': name_cont,
        }

        # contact = sock.execute(dbname, uid, pwd, 'res.partner', 'create', contact_dict)
        contact = create_or_update_contact(contact_dict)

    i += 1
