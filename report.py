# -*- coding: utf-8 -*-
import pandas as pd
import constants as const


def build(data, schedule, bl, hfr):
    # setup header and report dataframe
    header = const.HEADER.split(',')
    header.extend(const.SHIPPING_DATES)
    materials = pd.DataFrame(columns=header)

    # populate materials with inventory data
    materials[const.PN] = data[const.PN]
    materials[const.OH] = data[const.OH]
    materials[const.OO] = data[const.OO]
    materials[const.RO] = data[const.RO]

    # zero-out remaining columns
    materials[[const.BL, const.RLS, const.HFR, const.TA, const.RA]] = 0
    for row in materials.index:
        key = materials.loc[row, const.PN]
        if key in hfr and key in bl:
            materials.loc[row, const.HFR] = hfr[key]
            materials.loc[row, const.BL] = bl[key]
            materials.loc[row, const.RLS] = bl[key] - hfr[key]

        # calculate t-avail & r-avail
        ta = materials.loc[row, const.OH] + materials.loc[row, const.OO] - materials.loc[row, const.BL]
        materials.loc[row, const.TA] = ta
        materials.loc[row, const.RA] = materials.loc[row, const.TA] + materials.loc[row, const.HFR]

        # zero-out then fill shipping columns
        for j in range(const.SHIPPING_WIDTH):
            materials.iat[row, const.HEADER_WIDTH + j] = 0.0
        if key in schedule:
            for j in range(const.SHIPPING_WIDTH):
                values = schedule[key]
                materials.iat[row, const.HEADER_WIDTH + j] = values[j]

    # write file to disk
    writer = pd.ExcelWriter(const.DATAPATH + const.MATERIALS, engine=const.ENGINE)
    materials.to_excel(writer, sheet_name=const.SHEET, index=False)
    writer.save()
