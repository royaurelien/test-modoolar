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
dbname = "test_three"

# Connexion Odoo
sock_common = xmlrpclib.ServerProxy("http://odoo-domitec.yziact.net:8069/xmlrpc/common")
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy("http://odoo-domitec.yziact.net:8069/xmlrpc/object")

fich_ = open('BD_CLIENTS_GROUPE_API.csv', 'rb')

csvreader = csv.reader(fich_, delimiter=';')

tot = 0
i = 1

for row in csvreader:
    print i
    print row[0]
    if row[0] == "﻿CODE":
        i += 1
        continue



    name = row[16]

    customer = True
    supplier = False
    company_type = 'company'



    partner_dict = {
            'company_type': company_type,
            'name': name,

            'customer ': customer ,
            'supplier ': supplier ,
        }

    res_partner = sock.execute(dbname, uid, pwd, 'res.partner', 'create', partner_dict)
    print res_partner


    i += 1
