# -*- coding: utf-8 -*-
import inventory
import schedule as sch
import sales
import report
import constants as const


def run():
    data = inventory.build()
    hfr = sales.build(const.HOLD_FOR_RELEASE_AV_EXPORT)
    backlog = sales.build(const.BACKLOG_AV_EXPORT)
    schedule = sch.Schedule()
    schedule.display()
    report.build(data, schedule, backlog, hfr)
    print("Finished!")


if __name__ == "__main__":
    run()
