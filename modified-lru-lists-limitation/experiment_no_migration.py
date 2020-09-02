#!/usr/bin/env python3

"""
   experiment_no_migration.py

    Created on: Dec. 16, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
import time
from lib.amp import *
from lib.exptools import *
from lib.stats import *

workload_info_li = [
            ["speccpu2017", "607.cactuBSSN_s"],
            ["graph500", "graph500:bfs:23:16"],
            ["speccpu2017", "631.deepsjeng_s"],
            ["speccpu2017", "603.bwaves_s"],
        ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    parser.add_argument("-expname", default="modified-lru-lists-limitation")
    parser.add_argument("-keyword", default="no-migration")
    parser.add_argument("-monitor_interval", type=int, default="1")
    parser.add_argument("-transparent_hugepage", default="always")
    parser.add_argument("-migration_policy", type=int, default=MIG_POLICY_NOP)
    args = parser.parse_args()

    os.system("echo off | sudo tee /sys/devices/system/cpu/smt/control")
    os.system("echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
    os.system("echo 0 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo")
    os.system("echo 0 | sudo tee /proc/sys/kernel/numa_balancing")

    expname = "%s-tmp-%s" % (args.expname, args.keyword)
    result_dir = setup_exp_directory(args.result_dir, args.expname)
    ssh_client = get_ssh_client("127.0.0.1", 2222, "root", "random")
    ssh_client.exec_command("sudo echo 0 > /proc/sys/kernel/numa_balancing")
    for workload_info in workload_info_li:
        workload_type = workload_info[0]
        workload_name = workload_info[1]
        signature = "%s_%s_%s"\
                % (workload_name, args.keyword, args.transparent_hugepage)
        print("signature =", signature)

        ssh_client.exec_command("sudo echo %s > /sys/kernel/mm/transparent_hugepage/enabled"\
                % (args.transparent_hugepage))

        reset_docker(ssh_client)
        workload = get_workload(ssh_client, workload_type, workload_name)
        workload.create()
        for cgroup in workload.get_cgroup_li():
            cgroup.set_int("memory.migration.policy",
                    args.migration_policy)
        runinfo = workload.run()
        (stdin, stdout, stderr) = runinfo["channel"]

        stdout_file = open("%s/%s.stdout.txt" % (result_dir, signature), "w")
        stderr_file = open("%s/%s.stderr.txt" % (result_dir, signature), "w")
        while True:
            record_stats_per_cgroup(result_dir, signature, workload.get_cgroup_li(),
                    "memory.migration.stats.num_total_pages")
            record_stats_per_cgroup(result_dir, signature, workload.get_cgroup_li(),
                    "memory.migration.stats.num_page_migrations")
            record_stats_per_cgroup(result_dir, signature, workload.get_cgroup_li(),
                    "memory.migration.stats.num_accessed_pages")
            record_stats_per_cgroup(result_dir, signature, workload.get_cgroup_li(),
                    "memory.migration.stats.num_fast_memory_hit_pages")
            record_std(stdout, stdout_file)
            record_std(stderr, stderr_file)
            if exit_condition(stdout):
                record_std(stdout, stdout_file)
                record_std(stderr, stderr_file)
                break
            time.sleep(args.monitor_interval)
        stdout_file.close()
        stderr_file.close()

    ssh_client.close()

if __name__ == "__main__":
    main()
