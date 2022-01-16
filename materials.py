# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup
import constants as const
import schedule as sch


def get_backlog():
    pass


def get_inventory():
    pass


def build_report():
    pass


def run():
    schedule = sch.Schedule()
    schedule.display()
    print("Validated: {}".format(schedule.valid))


if __name__ == "__main__":
    run()
