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
    return hold_for_release_builder(filename)


def hold_for_release_builder(filename):
    hfr = {}
    h = pd.read_csv(const.DATAPATH + filename)
    for i in range(0, len(h.index)):
        key = h.iloc[i][0]
        value = h.iloc[i][1]
        factor = h.iloc[i][2]
        if key in hfr:
            hfr[key] = hfr[key] + value * factor
        else:
            hfr[key] = value
    return hfr
