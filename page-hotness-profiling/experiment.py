#!/usr/bin/env python3

"""
   experiment.py

    Created on: Sep. 20, 2018
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
import socket
import time
from lib.exptools import *
from lib.stats import *
from lib.sysfs import *
from workload_info import *

hostname = socket.gethostname()
workload_info_li = get_workload_info_li(hostname)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    parser.add_argument("-expname", default="page-hotness-profiling-access-frequency")
    parser.add_argument("-monitor_interval", type=int, default="1")
    parser.add_argument("-transparent_hugepage", default="always")
    parser.add_argument("-scanning_interval", type=int, default="4")
    args = parser.parse_args()

    os.system("echo off | sudo tee /sys/devices/system/cpu/smt/control")
    os.system("echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
    os.system("echo 0 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo")
    os.system("echo 0 | sudo tee /proc/sys/kernel/numa_balancing")

    expname = "%s-tmp" % (args.expname)
    result_dir = setup_exp_directory(args.result_dir, expname)
    ssh_client = get_ssh_client("127.0.0.1", 2222, "root", "random")
    ssh_client.exec_command("echo 0 | sudo tee /proc/sys/kernel/numa_balancing")
    prof_sysfs = sysfs(ssh_client, "/sys/kernel/mm/profd/")
    for workload_info in workload_info_li:
        workload_type = workload_info[0]
        workload_name = workload_info[1]
        signature = "%s_%s_%d" % (workload_name, args.transparent_hugepage, args.scanning_interval)
        print("signature =", signature)

        ssh_client.exec_command("echo %s | sudo tee /sys/kernel/mm/transparent_hugepage/enabled"\
                % (args.transparent_hugepage))

        reset_docker(ssh_client)
        workload = get_workload(ssh_client, workload_type, workload_name)
        workload.create()
        runinfo = workload.run()
        (stdin, stdout, stderr) = runinfo["channel"]

        prof_sysfs.set_int("scanning_interval", args.scanning_interval)
        prof_sysfs.set_int("hotness_metric", 2) # access frequency

        stdout_file = open("%s/%s.stdout.txt" % (result_dir, signature), "w")
        stderr_file = open("%s/%s.stderr.txt" % (result_dir, signature), "w")
        while True:
            record_stats_per_cgroup(result_dir, signature,
                    workload.get_cgroup_li(), "memory.hotness.access_freq.stats")
            record_std(stdout, stdout_file)
            record_std(stderr, stderr_file)
            if exit_condition(stdout):
                record_std(stdout, stdout_file)
                record_std(stderr, stderr_file)
                break
            time.sleep(args.monitor_interval)
        stdout_file.close()
        stderr_file.close()

        prof_sysfs.set_int("scanning.interval", 0)

    ssh_client.close()

if __name__ == "__main__":
    main()
