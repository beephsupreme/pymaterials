# -*- coding: utf-8 -*-
import pandas as pd
import constants as const


class Inventory:
    def __init__(self):
        self.inventory = build()
        self.length = self.inventory.index.stop
        self.width = 10

    def get_row(self, idx):
        return self.inventory.iloc[idx]

    def display(self):
        print("Inventory has {} rows.".format(self.length))


def build():
    return inventory_builder()


def inventory_builder():
    d = pd.read_csv(const.DATAPATH + const.INVENTORY)
    return d
