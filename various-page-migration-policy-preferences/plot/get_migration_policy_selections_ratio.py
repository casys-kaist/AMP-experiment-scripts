#!/usr/bin/env python3

"""
   get_migration_policy_selections_ratio.py

    Created on: Dec. 26, 2019
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
    file_path_li = glob(args.result_dir + "/*.mig_policy.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)
        workload_signature = filename.replace(".mig_policy.txt", "")
        if "amp" in workload_signature:
            fast_memory_ratio, thp, mig_policy, abbr_workload_name\
                    = parse_workload_signature(workload_signature)

            data_dict.update({abbr_workload_name:
                {MIG_POLICY_LRU: 0, MIG_POLICY_LFU: 0, MIG_POLICY_PSEUDO_RANDOM: 0}})
            with open("%s/%s" % (args.result_dir, filename)) as f:
                for line in f:
                    mig_policy = int(line.strip())
                    data_dict[abbr_workload_name][mig_policy] += 1

    for abbr_workload_name in data_dict.keys():
        num_selections_sum = 0
        for mig_policy in data_dict[abbr_workload_name].keys():
            num_selections_sum += data_dict[abbr_workload_name][mig_policy]
        for mig_policy in data_dict[abbr_workload_name].keys():
            data_dict[abbr_workload_name][mig_policy] /= num_selections_sum

    for abbr_workload_name in data_dict.keys():
        for mig_policy in data_dict[abbr_workload_name].keys():
            selection_ratios = data_dict[abbr_workload_name][mig_policy]
            result = "%s,%s,%f" % (abbr_workload_name, mig_policy, selection_ratios*100)
            print(result)

if __name__ == "__main__":
    main()
