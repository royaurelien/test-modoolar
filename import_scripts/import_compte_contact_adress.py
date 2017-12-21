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
    dbname = "DOM_20_12"

    sock_common = xmlrpclib.ServerProxy("http://192.168.100.139:8069/xmlrpc/common")
    uid = sock_common.login(dbname, username, pwd)
    sock = xmlrpclib.ServerProxy("http://192.168.100.139:8069/xmlrpc/object")


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




set_connexion_doodoo()
fich_ = open('../BD_CLIENTS_API.csv', 'rb')

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
    name = row[1]
    parent_bis = row[2]
    parent = row[3]
    city = row[5]
    country_id = row[6]
    blocked = row[18]
    zip = row[4].strip()
    phone = row[9]
    mobile = row[10]
    email = row[24]

    comment = 'rep : '+ row[7] + ' Famille : ' + row[17]

    if blocked == 'Oui':
        trust = 'bad'

    existe = partner_search(name)
    parent_id = recherche_parent(parent, parent_bis)



    if existe:
        name += ' (' + str(city) +')'

    tot += 1

    partner_dict = {
            'company_type': company_type,
            'trust': trust,
            'parent_id': parent_id,
            'customer ': customer,
            'supplier ': supplier,
            'is_company': is_company,
            'ref': ref,
            'name': name,
            'parent_bis': parent_bis,
            'parent': parent,
            'city': city,
            'country_id': country_id,
            'blocked':blocked,
            'zip': zip,
            'phone': phone,
            'mobile': mobile,
            'email': email,
            'comment': comment,
        }

    compte = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner_dict)

    # Champ pour adresses livraison
    type = 'delivery'
    parent_id_dev = compte
    name_dev = row[11]
    city_dev = row[12]
    cp_dev = row[13]
    addr1_dev = row[14]
    addr2_dev = row[15]
    comment_dev = row[16]

    livraison_dict = {
        'type':type,
        'parent_id':parent_id_dev ,
        'name':name_dev,
        'city':city_dev,
        'zip':cp_dev,
        'street':addr1_dev,
        'street2':addr2_dev,
        'comment':comment_dev,
    }

    livraison_adr = sock.execute(dbname, uid, pwd, 'res.partner', 'create', livraison_dict)

    # Champ pour adresses livraison
    type = 'invoice'
    parent_id_inv = compte
    name_inv = row[1] + 'Facturation'
    city_inv = row[5]
    zip_inv = row[4]
    street_inv = row[26]
    street2_inv = row[27]
    comment_inv = row[25]
    email_inv = row[23]

    facturation_dict = {
        'type': type,
        'parent_id': parent_id_inv,
        'name': name_inv,
        'city': city_inv,
        'zip': zip_inv,
        'street': street_inv,
        'street2': street2_inv,
        'comment': comment_inv,
        'email': email_inv,
    }

    facturation_adr = sock.execute(dbname, uid, pwd, 'res.partner', 'create', facturation_dict)

    type = 'contact'
    parent_id_inv = compte
    name_cont = row[8]

    contact_dict = {
        'type': type,
        'parent_id': parent_id_inv,
        'name': name_cont,
    }

    contact = sock.execute(dbname, uid, pwd, 'res.partner', 'create', contact_dict)

    i += 1

print 'TOT : ', tot
