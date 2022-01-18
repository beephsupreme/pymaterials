# -*- coding: utf-8 -*-
import pandas as pd
import constants as const


def build(data, schedule, bl, hfr):
    header = const.HEADER.split(',')
    header.extend(schedule.header)
    mats = pd.DataFrame(columns=header)
    mats[const.PN] = data[const.PN]
    mats[const.OH] = data[const.OH]
    mats[const.OO] = data[const.OO]
    mats[const.RO] = data[const.RO]
    mats[[const.BL, const.RLS, const.HFR, const.TA, const.RA]] = 0
    for i in mats.index:
        key = mats.loc[i, const.PN]
        if key in hfr and key in bl:
            mats.loc[i, const.HFR] = hfr[key]
            mats.loc[i, const.BL] = bl[key]
            mats.loc[i, const.RLS] = bl[key] - hfr[key]
        mats.loc[i, const.TA] = mats.loc[i, const.OH] + mats.loc[i, const.OO] - mats.loc[i, const.BL]
        mats.loc[i, const.RA] = mats.loc[i, const.TA] + mats.loc[i, const.HFR]
        for j in range(schedule.width):
            mats.iat[i, const.HEADER_WIDTH + j] = 0.0
        if schedule.valid_key(key):
            for j in range(schedule.width):
                values = schedule.schedule[key]
                mats.iat[i, const.HEADER_WIDTH + j] = values[j]
    writer = pd.ExcelWriter(const.DATAPATH + const.MATERIALS, engine=const.ENGINE)
    mats.to_excel(writer, sheet_name=const.SHEET, index=False)
    writer.save()
