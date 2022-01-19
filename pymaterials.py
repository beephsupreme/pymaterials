# -*- coding: utf-8 -*-
import inventory
import shipping
import sales
import report
import constants as const


def run():
    print("Loading files ...")
    data = inventory.build()
    hfr = sales.build(const.HOLD_FOR_RELEASE_AV_EXPORT)
    backlog = sales.build(const.BACKLOG_AV_EXPORT)
    schedule = shipping.build()
    report.build(data, schedule, backlog, hfr)
    print("Finished!")


if __name__ == "__main__":
    run()
