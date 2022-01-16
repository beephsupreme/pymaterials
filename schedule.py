# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup
import constants as const


def get_schedule():
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

    # get table header
    header = table[0]

    # convert quantites to float values
    for i in range(1, num_lines):
        for j in range(1, num_dates + 1):
            table[i][j] = float(table[i][j])

    # validate part numbers
    v = pd.read_csv(const.DATAPATH + const.VALIDATE, sep=',', lineterminator='\r')
    v.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["", ""], regex=True, inplace=True)
    validate = {}
    for i in range(0, len(v.index)):
        validate[v.iloc[i][0]] = v.loc[i][1]
    print(validate)

    d = pd.read_csv(const.DATAPATH + const.DATA, sep=',', lineterminator='\r')
    # file.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["", ""], regex=True, inplace=True)
    parts = []
    for i in range(0, len(d.index)):
        parts.append(d.iloc[i][0])
    print(parts)

    # create dictionary from table
    schedule = {}
    for i in range(1, num_lines):
        key = table[i][0]
        values = []
        for j in range(1, num_dates + 1):
            values.append(table[i][j])
        schedule[key] = values

    # translate values

    print(schedule)
