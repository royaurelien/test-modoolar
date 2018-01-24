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
dbname = "DOM_12_01"

# Connexion Odoo
sock_common = xmlrpclib.ServerProxy("http://192.168.100.139:8069/xmlrpc/common")
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy("http://192.168.100.139:8069/xmlrpc/object")


def recherche_partner(partner):
    if partner :
        partner_id = sock.execute(dbname, uid, pwd, 'res.partner', 'search_read', ([('name', '=', partner)]), ('id'))
        partner_id =  partner_id[0]['id']

    else:
        partner_id = False

    return partner_id


def recherche_iban(iban):
    if iban:
        iban = sock.execute(dbname, uid, pwd, 'res.partner.bank', 'search_read',([('acc_number','=',iban)]),('id'))

        if iban :
            iban_id = iban[0]['id']
        else :
            iban_id = False
    else:
        iban_id = False

    return iban_id


def recherche_bic(bic):
    if bic:
        bic = sock.execute(dbname, uid, pwd, 'res.bank', 'search_read',([('bic','=',bic)]),('id'))

        if bic:
            bic_id = bic[0]['id']
        else:
            bic_id = False

    else:
        bic_id = False

    return bic_id




fich_ = open('BD_CLIENTS_DEFINITIVE_API.csv', 'rb')

csvreader = csv.reader(fich_, delimiter=';')

tot = 0
i = 1

for row in csvreader:
    print i
    print row[1]
    bank_dict={}

    if row[30]:
        iban = row[30]
        existe = recherche_iban(iban)

        if not existe:
            bic = row[32]
            bank_id = recherche_bic(bic)


            partner = row[1]
            partner_id = recherche_partner(partner)
            if partner_id:
                bank_dict = {
                    'acc_number' :iban,
                    'bank_id':bank_id,
                    'partner_id':partner_id,
                }

                acc_bank_id = sock.execute(dbname, uid, pwd, 'res.partner.bank', 'create', bank_dict)
            tot +=1
    i+=1


print tot



