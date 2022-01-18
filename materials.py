# -*- coding: utf-8 -*-
import inventory
import schedule as sch
import sales
import report
import constants as const


def run():
    data = inventory.build()
    schedule = sch.Schedule()
    schedule.display()
    bl = sales.SalesData(const.BACKLOG)
    bl.display()
    hfr = sales.SalesData(const.HOLD_FOR_RELEASE)
    hfr.display()
    report.build(data, schedule, bl, hfr)
    print("Finished!")


if __name__ == "__main__":
    run()
