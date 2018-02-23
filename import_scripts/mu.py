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

fich_ = open('Grand livre v2.csv', 'rb')
fich_2 = open('test.csv','wb')

csvreader = csv.reader(fich_, delimiter=';')
csvwriter = csv.writer(fich_2, delimiter=';')

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
    print(i)
    compte = ''

    name = row[2]
    libel = row[6]

    if len(name) < 4:
        if  ':' in libel:
            libel1, libel2 = libel.split(':')
            compte, libel21 = libel2.split(',')

    if compte :
        row[2] = compte

    csvwriter.writerow(row)

fich_2.close()
fich_.close()
