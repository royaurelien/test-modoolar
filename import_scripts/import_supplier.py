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
    username = "admin"
    pwd = "X200yziact"
    dbname = "DOM_12_01"

    sock_common = xmlrpclib.ServerProxy("http://192.168.100.139:8069/xmlrpc/common")
    uid = sock_common.login(dbname, username, pwd)
    sock = xmlrpclib.ServerProxy("http://192.168.100.139:8069/xmlrpc/object")


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
        fam = sock.execute(dbname, uid, pwd, 'dom.famille_supplier', 'search_read', ([('name', '=', fam_name)]),('id'))
        if fam :
            fam_id=fam[0]['id']


    return fam_id


set_connexion_doodoo()
fich_ = open('fournisseurs_V2import.csv', 'rb')

csvreader = csv.reader(fich_, delimiter=';')

tot = 0
i = 1

type_rel = sock.execute(dbname, uid, pwd, 'crm_yzi.type_rel','search_read', ([('name', '=', 'Fournisseur')]), ('id'))

type_rel_id = type_rel[0]['id']

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
    country_id = row[10]
    website = row[12]
    famille = famille_raw[0].upper()+famille_raw[1:].lower()

    cond_reg_id = search_reg(cod_reg)
    famille_id = search_fam(famille)

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

    compte = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner_dict)

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

        contact = sock.execute(dbname, uid, pwd, 'res.partner', 'create', contact_dict)
    i += 1
