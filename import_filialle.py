#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmlrpclib
import csv
import sys
from datetime import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

username = "admin"
pwd = "X200yziact"
dbname = "test_one"

# Connexion Odoo
sock_common = xmlrpclib.ServerProxy("http://192.168.100.139:8069/xmlrpc/common")
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy("http://192.168.100.139:8069/xmlrpc/object")

fich_ = open('BD_CLIENTS_SOUS_GROUP.csv', 'rb')

csvreader = csv.reader(fich_, delimiter=';')

tot = 0
i = 1

for row in csvreader:
    print i
    print row[0]
    if i < 1 :
        i += 1
        continue


    company_type = 'company'

    name = row[3]
    name_id = False
    parent = row[2]
    parent_id = False

    customer = True
    supplier = False
    is_company = True

    if parent :
        parent_id=sock.execute(dbname, uid, pwd, 'res.partner', 'search_read',[('name','=',parent)], ('id'))
        print parent_id[0]['id']
        parent_id = parent_id[0]['id']

    if name:
        name_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search_read', [('name', '=', name)])

    if not name_id:
        tot += 1
        partner_dict = {
                'company_type': company_type,
                'name': name,
                'parent_id': parent_id,
                'customer ': customer ,
                'supplier ': supplier ,
                'is_company': is_company,
            }

        res_partner = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner_dict)



    i += 1

print 'TOT : ', tot
