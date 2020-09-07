#!/usr/bin/env python3

"""
   experiment.py

    Created on: Sep. 7, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
import time
from lib.exptools import *
from lib.stats import *

workload_info_li = [
        ["page_hotness_tracking_overhead_synthetic_bench", "page_hotness_tracking_overhead_synthetic_bench:8"],
        ["page_hotness_tracking_overhead_synthetic_bench", "page_hotness_tracking_overhead_synthetic_bench:16"],
        ["page_hotness_tracking_overhead_synthetic_bench", "page_hotness_tracking_overhead_synthetic_bench:24"],
        ["page_hotness_tracking_overhead_synthetic_bench", "page_hotness_tracking_overhead_synthetic_bench:32"],
    ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    parser.add_argument("-expname", default="page-hotness-tracking-overhead")
    parser.add_argument("-transparent_hugepage", default="always")
    args = parser.parse_args()

    os.system("echo off | sudo tee /sys/devices/system/cpu/smt/control")
    os.system("echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
    os.system("echo 0 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo")
    os.system("echo 0 | sudo tee /proc/sys/kernel/numa_balancing")

    expname = "%s-%s-tmp" % (args.expname, args.transparent_hugepage)
    result_dir = setup_exp_directory(args.result_dir, expname)
    ssh_client = get_ssh_client("127.0.0.1", 22, "root", "random")
    ssh_client.exec_command("echo 0 | sudo tee /proc/sys/kernel/numa_balancing")
    for workload_info in workload_info_li:
        workload_type = workload_info[0]
        workload_name = workload_info[1]
        signature = "%s_%s" % (workload_name, args.transparent_hugepage)
        print("signature =", signature)

        ssh_client.exec_command("echo %s | sudo tee /sys/kernel/mm/transparent_hugepage/enabled"\
                % (args.transparent_hugepage))

        reset_docker(ssh_client)
        workload = get_workload(ssh_client, workload_type, workload_name)
        workload.create()
        runinfo = workload.run()

        time.sleep(120)

        for i in range(5):
            record_stats_per_cgroup(result_dir, signature,
                    workload.get_cgroup_li(), "memory.migration.hotness_tracking.elapsed_time")

    ssh_client.close()

if __name__ == "__main__":
    main()
