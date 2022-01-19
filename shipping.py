# -*- coding: utf-8 -*-
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import constants as cn


def build(parts):
    page = get_page()
    table = get_table(page)
    table.append(['EX-CNT-VF', 20000.0, 0.0, 0.0])
    table.append(['EX-CNT-VF', 20000.0, 0.0, 0.0])
    table.append(['EX-CNT-VF', 20000.0, 0.0, 0.0])
    table.append(['EX-CNT-VF', 20000.0, 0.0, 0.0])
    table = validate_table(table, parts)
    table = translate_table(table)
    schedule = make_dictionary(table)
    cn.SHIPPING_DATES = (table[0])[1:]
    cn.SHIPPING_WIDTH = len(cn.SHIPPING_DATES)
    print("Schedule has {} unique entries.".format(cn.SCHEDULE_LENGTH))
    print("Shipping dates: {}".format(cn.SHIPPING_DATES))
    return schedule

    # return make_dictionary(table), table[0]


def get_page():
    html = requests.get(cn.SCHEDULE_URL)
    soup = BeautifulSoup(html.content, cn.PARSER)
    td = soup.find_all(cn.ELEMENT)
    page = []
    for line in td:
        text = line.get_text()
        if text == cn.WHITESPACE:
            text = cn.NEW_WHITESPACE
        page.append(text)
    return page


def get_table(page):
    # find FIRSTLINE_TEXT and remember index
    first_line = 0
    for first_line, d in enumerate(page):
        if d == cn.FIRSTLINE_TEXT:
            break
    # traverse backwards from FIRSTLINE_TEXT until blank found
    # then move forward 1 place where the first shipping date and remember the index
    first_date = 0
    for first_date in range(first_line, 0, -1):
        if page[first_date] == "":
            first_date += 1
            break
    # calculate number of shipping dates and width of table
    cn.SHIPPING_WIDTH = first_line - first_date
    line_length = cn.SHIPPING_WIDTH + cn.SCHEDULE_FIXED_FIELDS
    # move shipping dates to proper location
    for i in range(cn.SHIPPING_WIDTH):
        page[first_date + line_length + i] = page[first_line - cn.SHIPPING_WIDTH + i]
    # slice off everything before FIRSTLINE_TEXT
    page = page[first_line:]
    # calculate number of rows in table
    num_lines = (len(page) // line_length) - 1
    # convert list into table
    table = []
    for i in range(num_lines):
        line = []
        for j in range(line_length):
            line.append(page[i + i * (line_length - 1) + j])
        line = line[:1] + line[cn.SCHEDULE_FIXED_FIELDS:]
        table.append(line)
    # convert quantites to float values
    for i in range(1, num_lines):
        for j in range(1, cn.SHIPPING_WIDTH + 1):
            table[i][j] = float(table[i][j])
    return table


def validate_table(table, parts):
    # read VALIDATION_DB and load into a dictionary
    validate = {}
    v = pd.read_csv(cn.DATAFILE_PATH + cn.VALIDATION_DB)
    for row in range(0, len(v.index)):
        validate[v.iloc[row][0]] = v.iloc[row][1]
    # check schedule parts against inventory parts
    validated = True
    for row in range(1, len(table)):
        current = table[row][0]
        current = filter_parts(current)
        if current not in parts:
            if current in validate:
                table[row][0] = validate[current]
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
    t = pd.read_csv(cn.DATAFILE_PATH + cn.TRANSLATION_DB)
    for row in range(len(t.index)):
        translate[t.iloc[row][0]] = t.iloc[row][1]
    for row in range(1, len(table)):
        key = table[row][0]
        if key in translate:
            for col in range(1, len(table[0]) - 1):
                table[row][col] = table[row][col] * translate[key]
    return table


def make_dictionary(table):
    num_lines = len(table)
    num_dates = len(table[0]) - 1
    schedule = {}
    for row in range(1, num_lines):
        key = table[row][0]
        values = []
        for col in range(1, num_dates + 1):
            values.append(table[row][col])
        if key in schedule:
            old = schedule[key]
            new = values
            values = []
            for (o, n) in zip(old, new):
                values.append(o + n)
        schedule[key] = values
    cn.SCHEDULE_LENGTH = len(schedule)
    return schedule
