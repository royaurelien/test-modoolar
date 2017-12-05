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
    dbname = "test_one"

    sock_common = xmlrpclib.ServerProxy("http://odoo-domitec.yziact.net:8069/xmlrpc/common")
    uid = sock_common.login(dbname, username, pwd)
    sock = xmlrpclib.ServerProxy("http://odoo-domitec.yziact.net:8069/xmlrpc/object")


def recherche_parent(parent, parent_bis):
    if parent :
        parent_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search_read', ([('name', '=', parent)]), ('id'))
        if parent_id :
            parent_id =  parent_id[0]['id']
        else :
            parent_id = sock.execute(dbname, uid, pwd, 'res.partner', 'create',
                                     {'company_type': 'company', 'is_company': True, 'name': parent})

    elif parent_bis :
        parent_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search_read', ([('name', '=', parent_bis)]), ('id'))
        if parent_id:
            parent_id = parent_id[0]['id']
        else :
            parent_id = sock.execute(dbname, uid, pwd, 'res.partner', 'create',
                                     {'company_type': 'company', 'is_company': True, 'name': parent})


    else :
        parent_id = False

    return parent_id


def partner_search(name):
    name_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search_read', ([('name', '=', name)]), ('id'))

    if name_id:
        name_id = name_id[0]['id']

    return name_id




set_connexion_doodoo()
fich_ = open('contact_sugar.csv', 'rb')

csvreader = csv.reader(fich_, delimiter=';')

tot = 0
i = 1

for row in csvreader:
    print i
    print row[0]
    if i <= 2 :
        i += 1
        continue

    # champ pour le Compte
    company_type = 'person'
    trust = 'normal'
    customer = True
    supplier = False
    is_company = False

    title = row[0]
    name = row[1].strip() + ' ' + row[2].strip()
    name = name.strip()
    function = row[3]
    mobile = row[4]
    phone = row[5]
    street = row[7]
    city = row[8]
    zip = row[9].strip()
    country = row[10]
    email = row[12]

    parent = row[13]

    comment = 'lead source : '+ row[11]


    existe = partner_search(name)
    print 'MUUUUUUU', existe
    parent_id = recherche_parent(parent, False)

    if existe:
        i += 1
        continue

    tot += 1

    partner_dict = {
            'company_type': company_type,
            'trust': trust,
            'parent_id': parent_id,
            'customer ': customer,
            'supplier ': supplier,
            'is_company': is_company,
            'name': name,
            'parent': parent_id,
            'city': city,
            'country': country,
            'zip': zip,
            'phone': phone,
            'mobile': mobile,
            'email': email,
            'comment': comment,
        }

    compte = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner_dict)



    i += 1

print 'TOT : ', tot
