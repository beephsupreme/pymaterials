# -*- coding: utf-8 -*-
import pandas as pd
import constants as const


def build(filename):
    df = pd.read_csv(const.DATAPATH + filename)
    df.columns = [const.PN, const.BL, const.MP]
    df.loc[:, const.BL] = df.loc[:, const.BL] * df.loc[:, const.MP]
    df.drop(const.MP, axis=1, inplace=True)
    df = df.groupby([const.PN]).sum()
    dictionary = (df.to_dict())['Backlog']
    if filename == const.HOLD_FOR_RELEASE_AV_EXPORT:
        print("HFR has {} entries.".format(df.size))
    else:
        print("Backlog has {} entries.".format(df.size))
    return dictionary
