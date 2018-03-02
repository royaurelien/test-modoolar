#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmlrpclib
import csv
import sys
from datetime import datetime
import pprint


reload(sys)
sys.setdefaultencoding("utf-8")


# Connexion Odoo
username = "admin"
pwd = "X200yziact"
dbname = "DOM_07_02"

sock_common = xmlrpclib.ServerProxy("http://odoo-domitec.yziact.net:8069/xmlrpc/common")
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy("http://odoo-domitec.yziact.net:8069/xmlrpc/object")

def format_date(date_str):
    date = ''
    if not date_str :
        raise UserWarning('PAS de DATE')

    if '/' in date_str:
        day, month, year = date_str.split('/')

        date = year+'-'+month+'-'+day

    return date

fich_ = open('test.csv', 'rb')

csvreader = csv.reader(fich_, delimiter=';')

tot = 0
i = 1

dict_journaux = {
    'VE' : 1,
    'AC' : 2,
    'CEE' : 4,
    'CE' : 7,
    '90' : 9,
    'BS' : 10,
    'SAL' : 13,
    'FG' : 12,
}

list_move = []

for row in csvreader:
    if i <=1:
        i+=1
        continue

    tuple_ecriture = ()
    dict_ecriture = {}
    move_dict = {}
    debit = 0.0
    credit = 0.0

    date_str = row[0]
    date = format_date(date_str)
    name = row[2]
    # print(name)
    code_jour = row[3]
    journal_id = dict_journaux[code_jour]
    line_ids = []

    compte = row[1]
    libel = row[6]
    debit_str = (row[7].replace(',', '.')).replace(' ', '')
    credit_str = (row[8].replace(',', '.')).replace(' ', '')
    if debit_str:
        debit = float(debit_str)
    if credit_str:
        credit = float(credit_str)

    compte_id = sock.execute(dbname, uid, pwd, 'account.account', 'search', ([('code', '=', compte)]))
    if not compte_id:
        print(compte)
        continue

    dict_ecriture = {
        'date': date,
        'account_id': compte_id[0],
        'name': libel,
    }

    if str(debit) != '0.0':
        dict_ecriture['debit'] = debit

    if str(credit) != '0.0':
        dict_ecriture['credit'] = credit


    tuple_ecriture = (0, 0, dict_ecriture)

    j=0
    test = False
    for move in list_move:
        if move['name'] != name or move['journal_id'] != journal_id:
            j+=1
            # print(test)
        else:
            test = True
            # print(test)
            break

    if not test:
        line_ids.append(tuple_ecriture)
        move_dict ={
            'date':date,
            'name':name,
            'journal_id':journal_id,
            'line_ids':line_ids,
        }
        list_move.append(move_dict)
    else:
        # print(j)
        list_move[j]['line_ids'].append(tuple_ecriture)

    i+=1

fail = []
for move in list_move:
    # pprint.pprint(move)
    print(move['name'],move['journal_id'])
    if  move['name'] == '504bis' or move['name'] == '499'or move['name'] == '501' or move['name'] == '509':
        # move['name'] == '17092124' or or (len(move['name']) < 4 and move['journal_id'] == 10) or move['name'] == '497' or move['name'] == '496' or move['name'] == '498' or (0<len(move['name']) < 4 and move['journal_id'] == 10)
        fail.append((move['name'],move['journal_id']))
        continue

    sock.execute(dbname, uid, pwd, 'account.move', 'create', move)
    tot+=1


print(tot)
fich_.close()

pprint.pprint(fail)
