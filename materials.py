# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


def get_schedule():
    data = []
    url = 'https://www.toki.co.jp/purchasing/TLIHTML.files/sheet001.htm'
    path = './data/'

    print("Grab schedule...")
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    print("Extract data...")
    html_data = soup.find_all("table")[0].find_all("tr")[1:]

    print("Parse data...")
    for element in html_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)

    print("Format table...")
    df = pd.DataFrame(data=data)
    cols = len(df.columns)
    rows = len(df.index)
    ship_cols = cols - 5

    for i in range(1, ship_cols + 1):
        df.iloc[3, i + 4] = df.iloc[2, i]

    df = df.iloc[3:rows - 1]
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df = df.reset_index(drop=True)
    df = df.drop(['DESCRIPTION', 'P.O.#', 'note', 'VPC'], axis=1)

    df = df.replace("@", 0)
    df = df.replace(regex=r'^EX.$', value='EX-SPH-CL')

    print("Saving to disk...")
    writer = pd.ExcelWriter(path + '_schedule.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    print("Finished!")


def get_backlog():
    pass


def get_inventory():
    pass


def build_report():
    pass


if __name__ == "__main__":
    get_schedule()
