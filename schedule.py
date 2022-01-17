# -*- coding: utf-8 -*-
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup
import constants as const


class Schedule:
    def __init__(self):
        self.__schedule, self.header = build()
        self.length = len(self.__schedule)
        keys = list(self.__schedule.keys())
        key = keys[0]
        values = self.__schedule[key]
        self.width = len(values)

    def get_row(self, key):
        return self.__schedule.get(key)

    def valid_key(self, key):
        return key in list(self.__schedule.keys())

    def display(self):
        print("Shape: {}x{}".format(self.length, self.width))
        print("Header: {}".format(self.header))


def build():
    return schedule_builder()


def schedule_builder():
    page = get_page()
    table = get_table(page)
    table = validate_table(table)
    table = translate_table(table)
    return make_dictionary(table), table[0]


def get_page():
    # get page, parse content, get all <td> elements
    page = requests.get(const.URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    td = soup.find_all('td')
    # get text from td tags, insert "0" in blank fields
    data = []
    for i in range(0, len(td)):
        temp = td[i].get_text()
        if temp == "\u3000":
            temp = "0"
        data.append(temp)
    return data


def get_table(data):
    # find the start point in data
    first_line = 0
    for i in range(0, len(data)):
        if data[i] == const.FIRSTLINE_TEXT:
            first_line = i
            break
    # traverse backwards to find first shipping date
    first_date = 0
    for first_date in range(first_line, 0, -1):
        if data[first_date] == "":
            first_date += 1
            break
    # calculate number of shipping dates and width of table
    num_dates = first_line - first_date
    line_length = num_dates + const.SCHEDULE_WIDTH
    # move shipping dates to proper location
    for i in range(0, num_dates):
        data[first_date + line_length + i] = data[first_line - num_dates + i]
    # slice off everything before the start point, calculate number of useful table rows
    data = data[first_line:]
    num_lines = (len(data) // line_length) - 1
    # convert data list to list of lists
    table = []
    for i in range(0, num_lines):
        line = []
        for j in range(0, line_length):
            line.append(data[i + i * (line_length - 1) + j])
        line = line[:1] + line[5:]
        table.append(line)
    # convert quantites to float values
    for i in range(1, num_lines):
        for j in range(1, num_dates + 1):
            table[i][j] = float(table[i][j])
    return table


def validate_table(table):
    validate = {}
    v = pd.read_csv(const.DATAPATH + const.VALIDATE)
    for i in range(0, len(v.index)):
        validate[v.iloc[i][0]] = v.iloc[i][1]
    d = pd.read_csv(const.DATAPATH + const.DATA)
    parts = []
    for i in range(0, len(d.index)):
        parts.append(d.iloc[i][0])
    # check schedule parts against inventory parts
    validated = True
    for i in range(1, len(table)):
        current = table[i][0]
        if current not in parts:
            # print("{} not found in inventory.".format(current))
            if current in validate:
                table[i][0] = validate.get(current)
            else:
                print("{} not found.".format(current))
                validated = False
    if not validated:
        print("Errors occurred while validating the schedule.")
        # sys.exit(1)
    return table


def translate_table(table):
    translate = {}
    t = pd.read_csv(const.DATAPATH + const.TRANSLATE)
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
        schedule[key] = values
    return schedule
