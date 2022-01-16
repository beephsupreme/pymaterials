# -*- coding: utf-8 -*-
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup
import constants as const


class Schedule:

    def __init__(self):
        self.valid = False
        self.__schedule = build()
        self.length = len(self.__schedule)
        keys = list(self.__schedule.keys())
        self.width = 3  # len(keys[0])

    def get_row(self, key):
        return self.__schedule.get(key)

    def has_key(self, key):
        return key in list(self.__schedule.keys())

    def add(self, key, value):
        pass

    def replace(self, key, value):
        pass

    def accumulate(self, key, value):
        pass

    def display(self):
        print("Shape: {}x{}".format(self.length, self.width))
        print(self.__schedule)


def build():
    return schedule_builder()


def tranlate():
    pass


def schedule_builder():
    t = get_table()
    return t


def get_table():
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


def validate():
    # validate part numbers
    v = pd.read_csv(const.DATAPATH + const.VALIDATE)
    validate = {}
    for i in range(0, len(v.index)):
        validate[v.iloc[i][0]] = v.loc[i][1]

    d = pd.read_csv(const.DATAPATH + const.DATA)
    parts = []
    for i in range(0, len(d.index)):
        parts.append(d.iloc[i][0])

    # check schedule parts against inventory parts
    validated = True
    for i in range(1, num_lines):
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

    # translate values

    # create dictionary from table
    schedule = {}
    for i in range(1, num_lines):
        key = table[i][0]
        values = []
        for j in range(1, num_dates + 1):
            values.append(table[i][j])
        schedule[key] = values
    return schedule
