#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmlrpclib
import csv
import sys
from datetime import datetime, date

reload(sys)
sys.setdefaultencoding("utf-8")

def set_connexion_doodoo():
    global pwd
    global dbname
    global sock_common
    global uid
    global sock


username = "admin"
pwd = "X200yziact"
dbname = "test_two"

# Connexion Odoo
sock_common = xmlrpclib.ServerProxy("http://odoo-domitec.yziact.net:8069/xmlrpc/common")
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy("http://odoo-domitec.yziact.net:8069/xmlrpc/object")


def check_and_update(code, name):
    account_id = False
    if code and name :
        account = sock.execute(dbname, uid, pwd, 'account.account', 'search_read', ([('code','like', code)]),('id'))

        if account :
            account_id = account[0]['id']

            account = sock.execute(dbname, uid, pwd, 'account.account', 'write', [account_id], {'code':code, 'name':name})

    return account_id


def set_to_partner(account_id, account_name):
    update = False
    partner = False

    if account_id and account_name :
        partner = sock.execute(dbname, uid, pwd, 'res.partner', 'search_read', ([('name', '=',account_name)]), ('id'))
        account = sock.execute(dbname, uid, pwd, 'account.account', 'search_read', ([('id','=', account_id)]),(['user_type_id']))

        if partner and account :
            partner_id = partner[0]['id']
            account_type = account[0]['user_type_id']

            if account_type[0] == 1 or account_type[0] == 13 :

                sock.execute(dbname, uid, pwd, 'res.partner', 'write',[partner_id], {'property_account_receivable_id':account_id})
                update = True

            if account_type[0] == 2 :
                sock.execute(dbname, uid, pwd, 'res.partner', 'write', [partner_id], {'property_account_payable_id': account_id})
                update = True

    return update



fich_ = open('../plan_comptable.csv', 'rb')
csvreader = csv.reader(fich_, delimiter=';')
tot = 0
i = 1
account_type = {
'1': 11,
'2': 5,
'3': 5,
'401': 2,
'402': 2,
'403': 2,
'404': 2,
'405': 2,
'406': 2,
'407': 2,
'408': 2,
'409': 2,
'410': 2,
'411': 1,
'412': 1,
'413': 1,
'414': 1,
'415': 1,
'416': 1,
'417': 1,
'418': 1,
'419': 1,
'5': 3,
'6': 16,
'7': 14,
'8': 7,
'420-499': 13,
}




account_lines = []
for row in csvreader:
    line_dict = {}
    print i
    print row[0]
    if i <= 2:
        i += 1
        continue

    #code
    compte = row[0]
    #name
    nom = row[1]
    #reconcile (bool)
    reconcile = row[7]
    #montant debit ouverture compte
    debit = str(row[2])
    #montant credit ouverture compte
    credit = str(row[3])
    #tax par default
    # txTVA = row[4]

    acc = check_and_update(compte , nom)

    if not acc:
        first_letter = compte[0]

        if first_letter == '4':
            first_letter = compte[:3]

        type_id = account_type.get(first_letter, False)

        if not type_id:
            type_id = 1

        acc = sock.execute(dbname, uid, pwd,'account.account','create', {'code':compte, 'name':nom, 'reconcile':reconcile, 'user_type_id': type_id})


    if compte[0] == '4':
        up_partner = set_to_partner(acc, nom)


    if debit != '0,00':
        debit = float(debit.replace(',','.').replace(' ',''))
        line_dict_debit = {
            'account_id':acc,
            'debit': debit,
            'credit': 0.0,
        }
        account_lines.append((0, 0, line_dict_debit))

    if credit != '0,00':
        credit = float(credit.replace(',', '.').replace(' ', ''))
        line_dict_credit = {
            'account_id':acc,
            'debit': 0.0,
            'credit': credit,
        }
        account_lines.append((0,0,line_dict_credit))

    i += 1



today = date.today()
str_today = str(today)
account_move = {
    'date':str_today,
    'journal_id': 3, #joural des operations diverses
    'ref': '',
    'narration': "Ce movement a pour but de crediter/debiter tous les comptes importes dans odoo.",
    'line_ids': account_lines,
}

sock.execute(dbname, uid, pwd,'account.move','create', account_move)
