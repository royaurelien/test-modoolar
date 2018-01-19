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
    dbname = "test_three"

    sock_common = xmlrpclib.ServerProxy("http://odoo-domitec.yziact.net:8069/xmlrpc/common")
    uid = sock_common.login(dbname, username, pwd)
    sock = xmlrpclib.ServerProxy("http://odoo-domitec.yziact.net:8069/xmlrpc/object")


def recherche_parent(parent, parent_bis):
    if parent :
        parent_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search_read', ([('name', '=', parent)]), ('id'))
        parent_id =  parent_id[0]['id']

    elif parent_bis :
        parent_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search_read', ([('name', '=', parent_bis)]), ('id'))
        parent_id = parent_id[0]['id']
    else :
        parent_id = False

    return parent_id


def partner_search(name):
    name_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search_read', ([('name', '=', name)]), ('id'))

    if name_id:
        name_id = name_id[0]['id']

    return name_id

def search_remise(remise_str):
    remise = False
    if remise_str :
        remise = sock.execute(dbname, uid, pwd, 'dom.remise', 'search_read', ([('amount', '=', float(remise_str))]), ('id'))
        if remise:
            remise = remise[0]['id']

        else:
            remise = sock.execute(dbname, uid, pwd, 'dom.remise','create', {'amount':float(remise_str),'name':remise_str})

    return remise


set_connexion_doodoo()
fich_ = open('BD_CLIENTS_DEFINITIVE_API.csv', 'rb')

csvreader = csv.reader(fich_, delimiter=';')

tot = 0
i = 1

for row in csvreader:
    print i
    print row[0]
    if i <= 3 :
        i += 1
        continue

    # champ pour le Compte
    company_type = 'company'
    trust = 'normal'
    customer = True
    supplier = False
    is_company = True

    ref = row[0]
    code_api = row[0]
    name = row[1]
    city = row[2]
    zip = row[3].strip()
    website = row[6]
    phone = row[12]
    famille = row[14]
    parent_bis = row[15]
    parent = row[16]
    property_delivery_carrier_id = row[18]
    remise_str = str(row[20]).replace(',','.')
    bfa = row[26]
    user_id = row[35]

    # country_id = row[6]
    # blocked = row[18]
    # mobile = row[10]
    # email = row[24]

    if remise_str == '0':
        remise = False
    else:
        remise = search_remise(remise_str)

    # if blocked == 'Oui':
    #     trust = 'bad'

    existe = partner_search(name)
    parent_id = recherche_parent(parent, parent_bis)



    if existe:
        name += ' (' + str(city) +')'

    tot += 1

    # partner_dict = {
    #         'company_type': company_type,
    #         'trust': trust,
    #         'parent_id': parent_id,
    #         'customer ': customer,
    #         'supplier ': supplier,
    #         'is_company': is_company,
    #         'ref': ref,
    #         'name': name,
    #         'parent_bis': parent_bis,
    #         'parent': parent,
    #         'city': city,
    #         'country_id': country_id,
    #         'blocked':blocked,
    #         'zip': zip,
    #         'phone': phone,
    #         'mobile': mobile,
    #         'email': email,
    #         'comment': comment,
    #     }

    partner_dict = {
        'company_type':company_type,
        'is_company':is_company,
        'trust':trust,
        'customer':customer,
        'supplier':supplier,
        'ref':ref,
        'code_api':code_api,
        'name':name,
        'city':city,
        'zip':zip,
        'website':website,
        'phone':phone,
        'famille':famille,
        'parent_bis':parent_bis,
        'parent':parent,
        'property_delivery_carrier_id':property_delivery_carrier_id,
        'remise_str':remise_str,
        'bfa':bfa,
        'user_id':user_id,
    }

    compte = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner_dict)

    # Champ pour adresses livraison
    type = 'delivery'
    parent_id_dev = compte
    # name_dev = row[11]
    city_dev = row[7]
    addr1_dev = row[8]
    addr2_dev = row[9]
    cp_dev = row[10]
    mobile_dev = row[13]
    # comment_dev = row[16]


    livraison_dict = {
        'type':type,
        'parent_id':parent_id_dev ,
        # 'name':name_dev,
        'city':city_dev,
        'zip':cp_dev,
        'street':addr1_dev,
        'street2':addr2_dev,
        # 'comment':comment_dev,
    }

    livraison_adr = sock.execute(dbname, uid, pwd, 'res.partner', 'create', livraison_dict)

    # Champ pour adresses livraison
    type = 'invoice'
    parent_id_inv = compte
    # name_inv = row[1] + 'Facturation'
    # city_inv = row[5]
    # zip_inv = row[4]
    street_inv = row[23]
    street2_inv = row[24]
    # comment_inv = row[25]
    email_inv = row[28]

    facturation_dict = {
        'type': type,
        'parent_id': parent_id_inv,
        # 'name': name_inv,
        # 'city': city_inv,
        # 'zip': zip_inv,
        'street': street_inv,
        'street2': street2_inv,
        # 'comment': comment_inv,
        'email': email_inv,
    }

    facturation_adr = sock.execute(dbname, uid, pwd, 'res.partner', 'create', facturation_dict)

    if row[5]:
        type = 'contact'
        parent_id_inv = compte
        name_cont = row[5]

        contact_dict = {
            'type': type,
            'parent_id': parent_id_inv,
            'name': name_cont,
        }

        contact = sock.execute(dbname, uid, pwd, 'res.partner', 'create', contact_dict)

    if row[22]:
        type = 'contact'
        parent_id_inv = compte
        name_cont_compta = row[22]

        contact_fact_dict = {
            'type': type,
            'parent_id': parent_id_inv,
            'name': name_cont_compta,
        }

        contact_compta = sock.execute(dbname, uid, pwd, 'res.partner', 'create', contact_fact_dict)
        customer = sock.execute(dbname,uid,pwd, 'res.partner', 'write', compte, {'contact3':contact_compta})

    i += 1

print 'TOT : ', tot
