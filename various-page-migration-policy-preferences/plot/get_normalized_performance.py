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
from common import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    data_dict = {}
    file_path_li = glob(args.result_dir + "/*.stderr.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)
        workload_signature = filename.replace(".stderr.txt", "")
        fast_memory_ratio, thp, mig_policy, abbr_workload_name\
                = parse_workload_signature(workload_signature)

        elapsed_seconds = 0
        with open("%s/%s" % (args.result_dir, filename)) as f:
            for line in f:
                if "elapsed" in line and "CPU" in line:
                    elapsed_seconds = time_to_seconds(line)
        if elapsed_seconds != 0:
            if abbr_workload_name not in data_dict.keys():
                data_dict.update({abbr_workload_name: {"always": {}, "never": {}}})
            data_dict[abbr_workload_name][thp].update({mig_policy: elapsed_seconds})

    # normalize execution time
    baseline_thp = "always"
    baseline_mig_policy = "No Migration"
    for abbr_workload_name in data_dict.keys():
        for thp in data_dict[abbr_workload_name].keys():
            for mig_policy in data_dict[abbr_workload_name][thp].keys():
                if not ((thp == baseline_thp) and (mig_policy == baseline_mig_policy)):
                    data_dict[abbr_workload_name][thp][mig_policy]\
                            = (data_dict[abbr_workload_name][baseline_thp][baseline_mig_policy] * 100)\
                            / data_dict[abbr_workload_name][thp][mig_policy]
        data_dict[abbr_workload_name][baseline_thp][baseline_mig_policy] = 100

    # add ideal performance
    for abbr_workload_name in data_dict.keys():
        perf_li = []
        for mig_policy in data_dict[abbr_workload_name][baseline_thp].keys():
            if mig_policy != "No Migration":
                perf_li.append(data_dict[abbr_workload_name][baseline_thp][mig_policy])
        data_dict[abbr_workload_name][baseline_thp]["Ideal"] = max(perf_li)

    # print normalized performance
    for abbr_workload_name in data_dict.keys():
        for thp in data_dict[abbr_workload_name].keys():
            for mig_policy in data_dict[abbr_workload_name][thp].keys():
                normalized_performance = data_dict[abbr_workload_name][thp][mig_policy]
                result = "%s,%s,%s,%f" % (abbr_workload_name, thp, mig_policy, normalized_performance)
                print(result)

if __name__ == "__main__":
    main()
