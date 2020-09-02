#!/usr/bin/env python3

"""
   experiment.py

    Created on: Dec. 25, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
import time
from lib.amp import *
from lib.exptools import *
from lib.stats import *
from lib.util import *
from amp import *

workload_info_li = [
            ["page_migration_policy_preference_synthetic_bench",
                "mix"
                "+lru_favor:512000:4:20:193594924"
                "+lfu_favor:51200:0.5:401427297"],
            ["page_migration_policy_preference_synthetic_bench",
                "mix"
                "+lfu_favor:51200:0.5:401427297"
                "+lru_favor:512000:4:20:193594924"],
            ["page_migration_policy_preference_synthetic_bench",
                "mix"
                "+lru_favor:512000:4:20:193594924"
                "+random_favor:131072:105236354"],
            ["page_migration_policy_preference_synthetic_bench",
                "mix"
                "+lfu_favor:51200:0.5:401427297"
                "+random_favor:131072:105236354"],
            ["page_migration_policy_preference_synthetic_bench",
                "mix"
                "+random_favor:131072:105236354"
                "+lru_favor:512000:4:20:193594924"],
            ["page_migration_policy_preference_synthetic_bench",
                "mix"
                "+random_favor:131072:105236354"
                "+lfu_favor:51200:0.5:401427297"],
        ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    parser.add_argument("-expname", default="responsiveness-to-phase-transitions")
    parser.add_argument("-monitor_interval", type=int, default=1)
    parser.add_argument("-transparent_hugepage", default="always")
    parser.add_argument("-fast_memory_ratio", type=int, default=50)
    parser.add_argument("-migration_interval", type=int, default=5)
    parser.add_argument("-warm_up", type=int, default=3)
    parser.add_argument("-window_size", type=int, default=36)
    parser.add_argument("-random_threshold", type=float, default=0.2)
    args = parser.parse_args()

    os.system("echo off | sudo tee /sys/devices/system/cpu/smt/control")
    os.system("echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
    os.system("echo 0 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo")
    os.system("echo 0 | sudo tee /proc/sys/kernel/numa_balancing")

    expname = "%s-tmp" % (args.expname)
    result_dir = setup_exp_directory(args.result_dir, args.expname)

    ssh_client = get_ssh_client("127.0.0.1", 2222, "root", "random")
    ssh_client.exec_command("sudo echo 0 > /proc/sys/kernel/numa_balancing")
    for workload_info in workload_info_li:
        time.sleep(10)
        workload_type = workload_info[0]
        workload_name = workload_info[1]
        signature = "%s_%s_%d"\
                % (workload_name, args.transparent_hugepage, args.fast_memory_ratio)
        print("signature =", signature)

        ssh_client.exec_command("sudo echo %s > /sys/kernel/mm/transparent_hugepage/enabled"\
                % (args.transparent_hugepage))

        reset_docker(ssh_client)
        workload = get_workload(ssh_client, workload_type, workload_name)
        workload.create()
        for cgroup in workload.get_cgroup_li():
            cgroup.set_int("memory.migration.fast_memory_ratio",
                    args.fast_memory_ratio)

        runinfo = workload.run()
        (stdin, stdout, stderr) = runinfo["channel"]

        amp = AMP(result_dir, workload, signature,
                args.fast_memory_ratio, args.warm_up, args.window_size, args.random_threshold)

        num_switches = 0
        cnt = 3
        chosen_mig_policy = None
        stdout_file = open("%s/%s.stdout.txt" % (result_dir, signature), "w")
        stderr_file = open("%s/%s.stderr.txt" % (result_dir, signature), "w")
        while True:
            if (cnt % args.migration_interval) == 0:
                chosen_mig_policy = amp.choose_mig_policy()
                for cgroup in workload.get_cgroup_li():
                    cgroup.set_int("memory.migration.policy", chosen_mig_policy)
                    cgroup.set_int("memory.migration.do.scan", 1, validate=False)
                    cgroup.set_int("memory.migration.do.migrate_amp", 1, validate=False)
            cnt += 1

            if stdout.channel.recv_ready():
                line = stdout.channel.recv(32768).decode("utf-8")
                if "switch" in line:
                    print("switch")
                    if num_switches != 0:
                        record_stats_single(result_dir, signature, "mig_policy",
                                "switch\n")
                    num_switches += 1
                    cnt = 3

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
