# -*- coding: utf-8 -*-
import pandas as pd
import constants as const


class Inventory:
    def __init__(self):
        self.inventory = build()
        labels = [const.PN, const.OH, const.OO, const.RO]
        self.inventory.columns = labels
        self.length = self.inventory.index.stop


def build():
    data = pd.read_csv(const.DATAPATH + const.INVENTORY)
    print("Inventory has {} entries.".format(data.index.stop))
    return data
