# -*- coding: utf-8 -*-
import pandas as pd
import constants as const


def build():
    data = pd.read_csv(const.DATAPATH + const.INVENTORY_AV_EXPORT)
    data.columns = [const.PN, const.OH, const.OO, const.RO]
    print("Inventory has {} entries.".format(data.index.stop))
    return data
