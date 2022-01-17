# -*- coding: utf-8 -*-
import inventory
import schedule as sch
import sales
import report
import constants as const


def run():
    data = inventory.Inventory()
    data.display()
    schedule = sch.Schedule()
    schedule.display()
    bl = sales.SalesData(const.BACKLOG)
    bl.display()
    hfr = sales.SalesData(const.HOLD_FOR_RELEASE)
    hfr.display()
    materials = report.Materials(data, schedule, bl, hfr)
    materials.save()
    print("Finished!")


if __name__ == "__main__":
    run()
