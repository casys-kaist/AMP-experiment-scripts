#!/usr/bin/env python3

"""
   get_performance.py

    Created on: Jul. 27, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import sys
from lib.util import *
from lib.stats import *
sys.path.append("..")
from common import *
from workload_mix import *

keyword_li = ["no-migration", "lru", "lfu", "random", "amp"]

def get_mig_policy_name(policy):
    mig_policy_name_dict = {
                "no-migration": "No-Migration",
                "lru": "LRU",
                "lfu": "LFU",
                "random": "Random",
                "amp": "AMP"
            }
    return mig_policy_name_dict[policy]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    data_dict = {}
    for workload_mix in workload_mix_li:
        for keyword in keyword_li:
            workload_1_abbr_name = abbreviate_workload_name(refine_workload_name(workload_mix[0][1]))
            workload_2_abbr_name = abbreviate_workload_name(refine_workload_name(workload_mix[1][1]))
            if "no-migration" == keyword:
                signature = "%s_%s_%s_always" % (workload_1_abbr_name, workload_2_abbr_name, keyword)
            else:
                signature = "%s_%s_%s_always_50" % (workload_1_abbr_name, workload_2_abbr_name, keyword)
            workload_1_signature = "%s_0" % (signature)
            workload_2_signature = "%s_1" % (signature)

            with open("%s/%s.stderr.txt" % (args.result_dir, workload_1_signature)) as f:
                for line in f:
                    if "elapsed" in line:
                        workload_1_elapsed_time = time_to_seconds(line)

            with open("%s/%s.stderr.txt" % (args.result_dir, workload_2_signature)) as f:
                for line in f:
                    if "elapsed" in line:
                        workload_2_elapsed_time = time_to_seconds(line)

            workload_mix_name = "%s+%s" % (workload_1_abbr_name, workload_2_abbr_name)
            mig_policy = get_mig_policy_name(keyword)
            if workload_mix_name not in data_dict.keys():
                data_dict.update(
                        {workload_mix_name:
                            {
                                workload_1_abbr_name: {"No-Migration": None, "LRU": None, "LFU": None, "Random": None, "AMP": None},
                                workload_2_abbr_name: {"No-Migration": None, "LRU": None, "LFU": None, "Random": None, "AMP": None},
                            }})
            data_dict[workload_mix_name][workload_1_abbr_name][mig_policy] = workload_1_elapsed_time
            data_dict[workload_mix_name][workload_2_abbr_name][mig_policy] = workload_2_elapsed_time

    # normalize performance values
    for workload_mix_name in data_dict.keys():
        for workload_abbr_name in data_dict[workload_mix_name].keys():
            for mig_policy in data_dict[workload_mix_name][workload_abbr_name].keys():
                if mig_policy != "No-Migration":
                    elapsed_time = data_dict[workload_mix_name][workload_abbr_name][mig_policy]
                    data_dict[workload_mix_name][workload_abbr_name][mig_policy]\
                            = (data_dict[workload_mix_name][workload_abbr_name]["No-Migration"] * 100)\
                            / data_dict[workload_mix_name][workload_abbr_name][mig_policy]

    # print normalized performance values
    for workload_mix_name in data_dict.keys():
        for workload_abbr_name in data_dict[workload_mix_name].keys():
            for mig_policy in data_dict[workload_mix_name][workload_abbr_name].keys():
                if mig_policy != "No-Migration":
                    splitted_workload_mix_name = workload_mix_name.split("+")
                    idx = splitted_workload_mix_name.index(workload_abbr_name)
                    performance = data_dict[workload_mix_name][workload_abbr_name][mig_policy]
                    record = "%s,%s,%s,%f" % (workload_mix_name, idx, mig_policy, performance)
                    print(record)

if __name__ == "__main__":
    main()
