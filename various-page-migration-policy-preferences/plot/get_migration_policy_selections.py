#!/usr/bin/env python3

"""
   get_migration_policy_selections.py

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

            data_dict.update({abbr_workload_name: []})
            with open("%s/%s" % (args.result_dir, filename)) as f:
                for line in f:
                    mig_policy = line.strip()
                    data_dict[abbr_workload_name].append(mig_policy)

    for abbr_workload_name in data_dict.keys():
        result = "%s,%s"\
                % (abbr_workload_name, ",".join(data_dict[abbr_workload_name]))
        print(result)

if __name__ == "__main__":
    main()
