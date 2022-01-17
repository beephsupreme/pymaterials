# -*- coding: utf-8 -*-
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import constants as const


class Materials:
    def __init__(self, data, schedule, bl, hfr):
        self.__materials = build(data, schedule, bl, hfr)

    def save(self):
        writer = pd.ExcelWriter(const.DATAPATH + const.MATERIALS, engine='xlsxwriter')
        self.__materials.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()

    def display(self):
        print(self.__materials)


def build(data, schedule, bl, hfr):
    return build_report(data, schedule, bl, hfr)


def build_report(data, schedule, bl, hfr):
    header = const.HEADER.split(',')
    header.extend(schedule.header)
    mats = pd.DataFrame(columns=header)
    mats['Part Number'] = data.inventory['Part Number']
    mats['On Hand'] = data.inventory['QtyRealTimeOnHand']
    mats['On Order'] = data.inventory['QtyOnPurchaseOrder']
    mats['Reorder'] = data.inventory['Minimum_Stock_Level']
    mats[['Backlog', 'Released', 'HFR', 'T-Avail', 'R-Avail']] = 0

    for i in mats.index:
        key = mats.loc[i, 'Part Number']
        if hfr.valid_key(key) and bl.valid_key(key):
            mats.loc[i, 'HFR'] = hfr.sales[key]
            mats.loc[i, 'Backlog'] = bl.sales[key]
            mats.loc[i, 'Released'] = bl.sales[key] - hfr.sales[key]
        mats.loc[i, 'T-Avail'] = mats.loc[i, 'On Hand'] + mats.loc[i, 'On Order'] - mats.loc[i, 'Backlog']
        mats.loc[i, 'R-Avail'] = mats.loc[i, 'T-Avail'] + mats.loc[i, 'HFR']
        for j in range(0, schedule.width):
            mats.iat[i, 9 + j] = 0.0
        if schedule.valid_key(key):
            for j in range(0, schedule.width):
                values = schedule.schedule[key]
                mats.iat[i, 9 + j] = values[j]
    return mats
