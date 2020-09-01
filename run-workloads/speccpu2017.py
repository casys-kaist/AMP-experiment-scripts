#!/usr/bin/env python3

"""
   speccpu2017.py

    Created on: Apr. 11, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
import time
from lib.exptools import *
from lib.stats import *

workload_info_li = [
            ["speccpu2017", "600.perlbench_s"],
            ["speccpu2017", "602.gcc_s"],
            ["speccpu2017", "605.mcf_s"],
            ["speccpu2017", "620.omnetpp_s"],
            ["speccpu2017", "623.xalancbmk_s"],
            ["speccpu2017", "625.x264_s"],
            ["speccpu2017", "631.deepsjeng_s"],
            ["speccpu2017", "641.leela_s"],
            ["speccpu2017", "648.exchange2_s"],
            ["speccpu2017", "657.xz_s"],
            ["speccpu2017", "603.bwaves_s"],
            ["speccpu2017", "607.cactuBSSN_s"],
            ["speccpu2017", "619.lbm_s"],
            ["speccpu2017", "621.wrf_s"],
            ["speccpu2017", "627.cam4_s"],
            ["speccpu2017", "628.pop2_s"],
            ["speccpu2017", "638.imagick_s"],
            ["speccpu2017", "644.nab_s"],
            ["speccpu2017", "649.fotonik3d_s"],
            ["speccpu2017", "654.roms_s"],
        ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    parser.add_argument("-expname", default="run-speccpu2017")
    parser.add_argument("-monitor_interval", type=int, default="1")
    args = parser.parse_args()

    os.system("echo off | sudo tee /sys/devices/system/cpu/smt/control")
    os.system("echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
    os.system("echo 0 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo")
    os.system("echo 0 | sudo tee /proc/sys/kernel/numa_balancing")

    result_dir = setup_exp_directory(args.result_dir, args.expname)
    ssh_client = get_ssh_client("127.0.0.1", 2222, "root", "random")
    ssh_client.exec_command("echo 0 > /proc/sys/kernel/numa_balancing")
    for workload_info in workload_info_li:
        workload_type = workload_info[0]
        workload_name = workload_info[1]
        signature = "%s" % (workload_name)
        print("signature =", signature)

        reset_docker(ssh_client)
        workload = get_workload(ssh_client, workload_type, workload_name)
        workload.create()
        runinfo = workload.run()
        (stdin, stdout, stderr) = runinfo["channel"]

        stdout_file = open("%s/%s.stdout.txt" % (result_dir, signature), "w")
        stderr_file = open("%s/%s.stderr.txt" % (result_dir, signature), "w")
        while True:
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
