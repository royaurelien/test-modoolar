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

fich_ = open('BD_CLIENTS_AP_GROUP.csv', 'rb')

csvreader = csv.reader(fich_, delimiter=';')

tot = 0
i = 1

for row in csvreader:
    print i
    print row[0]
    if row[0] == "﻿CODE":
        i += 1
        continue


    company_type = 'company'

    name = row[2]

    customer = True
    supplier = False
    is_company = True


    partner_dict = {
            'company_type': company_type,
            'name': name,

            'customer ': customer ,
            'supplier ': supplier ,
            'is_company': is_company,
        }

    res_partner = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner_dict)
    print res_partner


    i += 1
