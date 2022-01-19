# -*- coding: utf-8 -*-
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import constants as const


def build():
    page = get_page()
    table = get_table(page)
    table = validate_table(table)
    table = translate_table(table)
    schedule = make_dictionary(table)
    const.SCHEDULE_LENGTH = len(table) - 1
    const.SHIPPING_DATES = (table[0])[1:]
    const.SHIPPING_WIDTH = len(const.SHIPPING_DATES)
    print("Schedule has {} unique entries.".format(const.SCHEDULE_LENGTH))
    print("Shipping dates: {}".format(const.SHIPPING_DATES))
    return schedule

    # return make_dictionary(table), table[0]


def get_page():
    page = requests.get(const.SCHEDULE_URL)
    soup = BeautifulSoup(page.content, const.PARSER)
    td = soup.find_all(const.ELEMENT)
    data = []
    for line in td:
        text = line.get_text()
        if text == const.WHITESPACE:
            text = const.NEW_WHITESPACE
        data.append(text)
    return data


def get_table(data):
    # find the start point in data
    first_line = 0
    for first_line, d in enumerate(data):
        if d == const.FIRSTLINE_TEXT:
            break
    # traverse backwards until blank found, forward 1 place to find first shipping date
    first_date = 0
    for first_date in range(first_line, 0, -1):
        if data[first_date] == "":
            first_date += 1
            break
    # calculate number of shipping dates and width of table
    num_dates = first_line - first_date
    line_length = num_dates + const.SCHEDULE_FIXED_FIELDS
    # move shipping dates to proper location
    for i in range(num_dates):
        data[first_date + line_length + i] = data[first_line - num_dates + i]
    # slice off everything before the start point, calculate number of useful table rows
    data = data[first_line:]
    num_lines = (len(data) // line_length) - 1
    # convert data list to list of lists
    table = []
    for i in range(num_lines):
        line = []
        for j in range(line_length):
            line.append(data[i + i * (line_length - 1) + j])
        line = line[:1] + line[const.SCHEDULE_FIXED_FIELDS:]
        table.append(line)
    # convert quantites to float values
    for i in range(1, num_lines):
        for j in range(1, num_dates + 1):
            table[i][j] = float(table[i][j])
    return table


def validate_table(table):
    validate = {}
    v = pd.read_csv(const.DATAPATH + const.VALIDATION_DB)
    for i in range(0, len(v.index)):
        validate[v.iloc[i][0]] = v.iloc[i][1]
    d = pd.read_csv(const.DATAPATH + const.INVENTORY_AV_EXPORT)
    parts = []
    for i in range(0, len(d.index)):
        parts.append(d.iloc[i][0])
    # check schedule parts against inventory parts
    validated = True
    for i in range(1, len(table)):
        current = table[i][0]
        current = filter_parts(current)
        if current not in parts:
            if current in validate:
                table[i][0] = validate.get(current)
            else:
                print("{} not found.".format(current))
                validated = False
    if not validated:
        print("Errors occurred while validating the schedule.")
        sys.exit(1)
    return table


def filter_parts(current):
    if "RV-SEALANT" in current:
        current = "RV-SEALANT"
    elif "Sample" in current:
        current = "Sample"
    elif "EX-SPH-CL" in current:
        current = "EX-SPH-CL"
    elif "EX-SPH-FR" in current:
        current = "EX-SPH-FR"
    elif "EX-G14-CL" in current:
        current = "EX-G14-CL"
    elif "EX-G14-FR" in current:
        current = "EX-G14-FR"
    elif "EX-S14-CL" in current:
        current = "EX-S14-CL"
    elif "EX-S14-FR" in current:
        current = "EX-S14-FR"
    return current


def translate_table(table):
    translate = {}
    t = pd.read_csv(const.DATAPATH + const.TRANSLATION_DB)
    for i in range(0, len(t.index)):
        translate[t.iloc[i][0]] = t.iloc[i][1]
    for i in range(1, len(table)):
        key = table[i][0]
        if key in translate:
            for j in range(1, len(table[0]) - 1):
                table[i][j] = table[i][j] * translate[key]
    return table


def make_dictionary(table):
    num_lines = len(table)
    num_dates = len(table[0]) - 1
    schedule = {}
    for i in range(1, num_lines):
        key = table[i][0]
        values = []
        for j in range(1, num_dates + 1):
            values.append(table[i][j])
        if key in schedule:
            old = schedule[key]
            new = values
            values = []
            for (o, n) in zip(old, new):
                values.append(o + n)
        schedule[key] = values
    return schedule
