#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import re
from openpyxl import Workbook
from collections import defaultdict
import pymssql


server = 'BJ-SQL02.fihtdc.com'
user='nString'
password='Nstring123456'

class TranslateItem(object):
    def __init__(self, account, project, feature, textid, langcode,
            translation):
        self.account = account
        self.project = project
        self.feature = feature
        self.textid = textid
        self.langcode = langcode
        self.translation = translation

class TransExport(object):
    def _get_lancode_set(self, translations):
        '''
        :type:
            translation: list of TranslateItem
        :rtype: 
            set contains all langcode
        '''
        lancode_set = set()
        for trans in translations:
            lancode_set.add(trans.langcode)

        return lancode_set

    def _get_id_map(self, translations):
        '''
        :type:
            translation: list of TranslateItem
        :rtype: 
            dict which map textid and all its translation
        '''
        id_map = defaultdict(list)
        for trans in translations:
            id_map[trans.textid].append(trans)

        return id_map

               
    def convert_trans_bytextids(self, textids, t2_xlsx):
        with pymssql.connect(server, user, password, 'nstring',charset='utf8')\
            as conn:

            with conn.cursor(as_dict=True) as cursor:
                sql_ids = str(tuple(textids))
                sql = "select Text, Account, Project, Feature, Language, Lv1 \
                from TranslationView where Account='KAIOS_UPDATE' and Text in " \
                + sql_ids

                cursor.execute(sql)

                lines = []
                translations = []
                for row in cursor:
                    trans_item = \
                    TranslateItem(row['Account'], row['Project'],
                    row['Feature'],row['Text'], row['Language'],
                    row['Lv1'])

                    translations.append(trans_item)

                self.save_trans_t2_v2(translations, t2_xlsx)

    def convert_trans_byaccount(self, t2_xlsx):
        server = 'BJ-SQL02.fihtdc.com'
        user='nString'
        password='Nstring123456'

        account = 'S30subcont'
        project = 'simplex4'
        with pymssql.connect(server, user, password, 'nstring',charset='utf8')\
            as conn:
            with conn.cursor(as_dict=True) as cursor:

                sql = "select Text, Account, Project, Feature, Language, Lv1 \
                from TranslationView where Account='{0}' and \
                Project='{1}'".format(account, project)

                cursor.execute(sql)

                lines = []
                translations = []
                for row in cursor:
                    trans_item = \
                    TranslateItem(row['Account'], row['Project'],
                    row['Feature'],row['Text'], row['Language'],
                    row['Lv1'])

                    translations.append(trans_item)

                self.save_trans_t2_v2(translations, t2_xlsx)



    def get_textids(self, fname = 'tb_searched.txt'):
        textids = []
        with open(fname,'r',encoding='utf8') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    textids.append(line)

        return textids


    def save_trans_t2_v2(self, translations, t2_xlsx):
        # don't map lancode and langmap in this version
        id_map = self._get_id_map(translations)
        lancode_set = self._get_lancode_set(translations)

        wb = Workbook()
        ws = wb.active

        # create map from langcode to column index in xlsx
        # fill title row 
        cur_row = 1
        cur_col = 1
        ws.cell(row=cur_row, column=cur_col).value = 'RefName' 
        col_map = {'RefName':cur_col}
        cur_col += 1
        ws.cell(row=cur_row, column=cur_col).value = 'ModOP' 
        col_map['ModOP'] = cur_col

        for code in sorted(lancode_set):
            cur_col += 1
            ws.cell(row=cur_row, column=cur_col).value = code
            col_map[code] = cur_col 

        # fill translation row
        for textid in sorted(id_map.keys()):
            cur_row += 1
            cur_col = col_map['RefName']
            ws.cell(row=cur_row, column=cur_col).value = textid
            cur_col = col_map['ModOP']
            ws.cell(row=cur_row, column=cur_col).value = \
                    id_map[textid][0].feature
            for trans in id_map[textid]:
                cur_col = col_map[trans.langcode]
                ws.cell(row=cur_row, column=cur_col).value = trans.translation

        wb.save(t2_xlsx)


