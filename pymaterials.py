# -*- coding: utf-8 -*-
import inventory
import shipping
import sales
import report
import constants as cn


def run():
    print("Loading files ...")
    data = inventory.build()
    hfr = sales.build(cn.HFR_EXPORT)
    backlog = sales.build(cn.BACKLOG_EXPORT)
    schedule = shipping.build(data[cn.PN].tolist())
    report.build(data, schedule, backlog, hfr)
    print("Finished!")


if __name__ == "__main__":
    run()
