#!/usr/bin/env python3

"""
   get_feature_gap_performance.py

    Created on: Nov. 25, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
from glob import glob
from lib.stats import *
from common import *

def get_feature_sum(result_dir, workload_signature, feature_name):
    feature_sum = 0
    file_path = "%s/%s_0.memory.migration.stats.%s.txt"\
            % (result_dir, workload_signature, feature_name)
    with open(file_path) as f:
        for line in f:
            feature_sum += int(line.strip())
    return feature_sum

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

        if (mig_policy != "No Migration") and (mig_policy != "AMP"):
            num_total_pages = get_feature_sum(args.result_dir, workload_signature, "num_total_pages")
            num_page_migrations = get_feature_sum(args.result_dir, workload_signature, "num_page_migrations")
            num_accessed_pages = get_feature_sum(args.result_dir, workload_signature, "num_accessed_pages")
            num_fast_memory_hit_pages = get_feature_sum(args.result_dir, workload_signature, "num_fast_memory_hit_pages")

            page_migration_stability = (num_total_pages - num_page_migrations) / num_total_pages
            accessed_page_ratio = num_accessed_pages / num_total_pages
            fast_memory_hit_ratio = num_fast_memory_hit_pages / num_total_pages
            if (num_accessed_pages != 0):
                fast_memory_access_ratio = num_fast_memory_hit_pages / num_accessed_pages
            else:
                fast_memory_access_ratio = 0
            reward = 0.1 * page_migration_stability + 0.54 * accessed_page_ratio + 0.36 * fast_memory_access_ratio

            elapsed_seconds = 0
            file_path = "%s/%s" % (args.result_dir, filename)
            with open(file_path) as f:
                for line in f:
                    if "elapsed" in line and "CPU" in line:
                        elapsed_seconds = time_to_seconds(line)
            if elapsed_seconds != 0:
                if abbr_workload_name not in data_dict.keys():
                    data_dict.update({abbr_workload_name: {"always": {}, "never": {}}})
                data_dict[abbr_workload_name][thp].update(
                        {mig_policy:
                            {"Elapsed Time": elapsed_seconds,
                             "Normalized Performance": None,
                             "Page Migration Stability": page_migration_stability,
                             "Accessed Page Ratio": accessed_page_ratio,
                             "Fast Memory Hit Ratio": fast_memory_hit_ratio,
                             "Fast Memory Access Ratio": fast_memory_access_ratio,
                             "Reward": reward,
                             "Page Migration Stability Gap": page_migration_stability,
                             "Accessed Page Ratio Gap": accessed_page_ratio,
                             "Fast Memory Hit Ratio Gap": fast_memory_hit_ratio,
                             "Fast Memory Access Ratio Gap": fast_memory_access_ratio,
                             "Reward Gap": reward}})

    # normalize performance
    for abbr_workload_name in data_dict.keys():
        # find the best-performing configuration
        config_li = []
        elapsed_time_li = []
        for thp in data_dict[abbr_workload_name].keys():
            for mig_policy in data_dict[abbr_workload_name][thp].keys():
                config_li.append([thp, mig_policy])
                elapsed_time_li.append(data_dict[abbr_workload_name][thp][mig_policy]["Elapsed Time"])
        idx = elapsed_time_li.index(min(elapsed_time_li))
        max_perf_thp = config_li[idx][0]
        max_perf_mig_policy = config_li[idx][1]

        # normalize performance
        for thp in data_dict[abbr_workload_name].keys():
            for mig_policy in data_dict[abbr_workload_name][thp].keys():
                data_dict[abbr_workload_name][thp][mig_policy]["Normalized Performance"]\
                        = (data_dict[abbr_workload_name][max_perf_thp][max_perf_mig_policy]["Elapsed Time"] * 100)\
                        / data_dict[abbr_workload_name][thp][mig_policy]["Elapsed Time"]

                data_dict[abbr_workload_name][thp][mig_policy]["Page Migration Stability Gap"]\
                        = data_dict[abbr_workload_name][max_perf_thp][max_perf_mig_policy]["Page Migration Stability"]\
                        - data_dict[abbr_workload_name][thp][mig_policy]["Page Migration Stability"]
                data_dict[abbr_workload_name][thp][mig_policy]["Accessed Page Ratio Gap"]\
                        = data_dict[abbr_workload_name][max_perf_thp][max_perf_mig_policy]["Accessed Page Ratio"]\
                        - data_dict[abbr_workload_name][thp][mig_policy]["Accessed Page Ratio"]
                data_dict[abbr_workload_name][thp][mig_policy]["Fast Memory Hit Ratio Gap"]\
                        = data_dict[abbr_workload_name][max_perf_thp][max_perf_mig_policy]["Fast Memory Hit Ratio"]\
                        - data_dict[abbr_workload_name][thp][mig_policy]["Fast Memory Hit Ratio"]
                data_dict[abbr_workload_name][thp][mig_policy]["Fast Memory Access Ratio Gap"]\
                        = data_dict[abbr_workload_name][max_perf_thp][max_perf_mig_policy]["Fast Memory Access Ratio"]\
                        - data_dict[abbr_workload_name][thp][mig_policy]["Fast Memory Access Ratio"]
                data_dict[abbr_workload_name][thp][mig_policy]["Reward Gap"]\
                        = data_dict[abbr_workload_name][max_perf_thp][max_perf_mig_policy]["Reward"]\
                        - data_dict[abbr_workload_name][thp][mig_policy]["Reward"]

    # print feature value gap and normalized performance
    for abbr_workload_name in data_dict.keys():
        for thp in data_dict[abbr_workload_name].keys():
            for mig_policy in data_dict[abbr_workload_name][thp].keys():
                for feature_name in ["Page Migration Stability Gap", "Accessed Page Ratio Gap", "Fast Memory Hit Ratio Gap", "Fast Memory Access Ratio Gap", "Reward Gap"]:
                    perf = data_dict[abbr_workload_name][thp][mig_policy]["Normalized Performance"]
                    feature_gap = data_dict[abbr_workload_name][thp][mig_policy][feature_name]
                    result = "%s,%s,%s,%s,%f,%f" % (abbr_workload_name, thp, mig_policy, feature_name.replace(" Gap", ""), feature_gap, perf)
                    print(result)

if __name__ == "__main__":
    main()

