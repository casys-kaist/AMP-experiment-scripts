#!/usr/bin/env python3

"""
   get_normalized_performance.py

    Created on: Dec. 16, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
from glob import glob
from lib.stats import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    workload_name_perf_dict = {}
    file_path_li = glob(args.result_dir + "/*.stderr.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)
        workload_signature = filename.replace(".stderr.txt", "")
        splitted_workload_signature = workload_signature.split("_")
        if "no-migration" in workload_signature:
            key = "no-migration"
            workload_name = "_".join(splitted_workload_signature[:-2])
            workload_name = workload_name.split(":")[0].replace("_0", "")
            workload_name = abbreviate_workload_name(workload_name)
        else:
            inact_scan_ratio = int(splitted_workload_signature[-1])
            act_scan_ratio = int(splitted_workload_signature[-2])
            slow_memory_ratio = splitted_workload_signature[-3]
            transparent_hugepage = splitted_workload_signature[-4]
            keyword = splitted_workload_signature[-5]
            workload_name = "_".join(splitted_workload_signature[:-5])
            workload_name = workload_name.split(":")[0].replace("_0", "")
            workload_name = abbreviate_workload_name(workload_name)
            key = "%d-%d" % (act_scan_ratio, inact_scan_ratio)

        elapsed_seconds = 0
        with open(file_path) as f:
            for line in f:
                if "elapsed" in line and "CPU" in line:
                    elapsed_seconds = time_to_seconds(line)

        if workload_name not in workload_name_perf_dict.keys():
            workload_name_perf_dict.update({workload_name: {}})
        workload_name_perf_dict[workload_name].update({key: elapsed_seconds})

    for workload_name in workload_name_perf_dict.keys():
        for key in workload_name_perf_dict[workload_name].keys():
            if key != "no-migration":
                workload_name_perf_dict[workload_name][key] =\
                        (workload_name_perf_dict[workload_name]["no-migration"] * 100)\
                        / workload_name_perf_dict[workload_name][key]
        workload_name_perf_dict[workload_name]["no-migration"] = 100

    for workload_name in workload_name_perf_dict.keys():
        for key in workload_name_perf_dict[workload_name].keys():
            if key != "no-migration":
                print("%s,%d,%d,%f"\
                        % (workload_name,
                            int(key.split("-")[0]), int(key.split("-")[1]),
                            workload_name_perf_dict[workload_name][key]))

if __name__ == "__main__":
    main()
