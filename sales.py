# -*- coding: utf-8 -*-
import pandas as pd
import constants as const


class SalesData:
    def __init__(self, filename):
        self.__name = ""
        if filename == "bl.txt":
            self.__name = "Backlog"
        elif filename == "hfr.txt":
            self.__name = "HoldForRelease"
        else:
            self.__name = filename
        self.sales = build(filename)
        self.length = len(self.sales)

    def display(self):
        print("{} has {} entries.".format(self.__name, self.length))

    def get_val(self, key):
        return self.sales.get(key)

    def valid_key(self, key):
        return key in list(self.sales.keys())


def build(filename):
    hfr = {}
    h = pd.read_csv(const.DATAPATH + filename)
    for i in range(h.shape[0]):
        key = h.loc[i, 'Part Number']
        value = h.loc[i, 'Qty Ordered']
        factor = h.loc[i, 'UM_Multiplier']
        if key in hfr:
            hfr[key] = hfr[key] + value * factor
        else:
            hfr[key] = value
    return hfr
