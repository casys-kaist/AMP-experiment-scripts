#!/usr/bin/env python3

"""
   experiment_no_migration.py

    Created on: Jan. 08, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
import time
from lib.amp import *
from lib.exptools import *
from lib.stats import *
from common import *
from workload_mix import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    parser.add_argument("-expname", default="multi-programmed-environment")
    parser.add_argument("-keyword", default="no-migration")
    parser.add_argument("-monitor_interval", type=int, default=1)
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
    for workload_mix in workload_mix_li:
        # workload signature
        workload_1_abbr_name = abbreviate_workload_name(refine_workload_name(workload_mix[0][1]))
        workload_2_abbr_name = abbreviate_workload_name(refine_workload_name(workload_mix[1][1]))
        signature = "%s_%s_%s_%s" % (workload_1_abbr_name, workload_2_abbr_name, args.keyword, args.transparent_hugepage)
        print("signature =", signature)

        ssh_client.exec_command("sudo echo %s > /sys/kernel/mm/transparent_hugepage/enabled"\
                % (args.transparent_hugepage))

        # create workload and per-workload signature
        workload_li = []
        workload_signature_li = []
        stdout_file_li = []
        stderr_file_li = []
        reset_docker(ssh_client)
        for i, workload_info in enumerate(workload_mix):
            workload_type = workload_info[0]
            workload_name = workload_info[1]
            workload = get_workload(ssh_client, workload_type, workload_name)
            workload.create()
            for cgroup in workload.get_cgroup_li():
                cgroup.set_int("memory.migration.policy",
                        args.migration_policy)
            workload_li.append(workload)
            workload_signature = "%s_%d" % (signature, i)
            workload_signature_li.append(workload_signature)
            stdout_file = open("%s/%s.stdout.txt" % (result_dir, workload_signature), "w")
            stderr_file = open("%s/%s.stderr.txt" % (result_dir, workload_signature), "w")
            stdout_file_li.append(stdout_file)
            stderr_file_li.append(stderr_file)

        # run workloads
        runinfo_li = []
        for workload in workload_li:
            runinfo_li.append(workload.run())

        # monitor workloads
        exit = False
        exited_idx = []
        num_exited_procs = 0
        while not exit:
            for i, workload in enumerate(workload_li):
                workload_signature = workload_signature_li[i]
                record_stats_per_cgroup(result_dir, workload_signature, workload.get_cgroup_li(),
                        "memory.migration.stats.num_total_pages")
                record_stats_per_cgroup(result_dir, workload_signature, workload.get_cgroup_li(),
                        "memory.migration.stats.num_page_migrations")
                record_stats_per_cgroup(result_dir, workload_signature, workload.get_cgroup_li(),
                        "memory.migration.stats.num_accessed_pages")
                record_stats_per_cgroup(result_dir, workload_signature, workload.get_cgroup_li(),
                        "memory.migration.stats.num_fast_memory_hit_pages")

            # check exit conditions
            for i, runinfo in enumerate(runinfo_li):
                (stdin, stdout, stderr) = runinfo["channel"]
                if i not in exited_idx:
                    if exit_condition(stdout):
                        exited_idx.append(i)
                        num_exited_procs += 1
                        if num_exited_procs == len(workload_mix):
                            exit = True
                stdout_file = stdout_file_li[i]
                stderr_file = stderr_file_li[i]
                record_std(stdout, stdout_file)
                record_std(stderr, stderr_file)

            time.sleep(args.monitor_interval)

        # record stdout and stderr
        for i, runinfo in enumerate(runinfo_li):
            (stdin, stdout, stderr) = runinfo["channel"]
            stdout_file = stdout_file_li[i]
            stderr_file = stderr_file_li[i]
            record_std(stdout, stdout_file)
            record_std(stderr, stderr_file)
            stdout_file.close()
            stderr_file.close()

    ssh_client.close()

if __name__ == "__main__":
    main()
