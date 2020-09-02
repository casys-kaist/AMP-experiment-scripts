#!/Usr/bin/env python3

"""
   get_migration_policy_selections.py

    Created on: Sep. 12, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
from glob import glob
from lib.amp import *
from lib.stats import *
from common import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    file_path_li = glob(args.result_dir + "/*.mig_policy.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)
        workload_signature = filename.replace(".mig_policy.txt", "")

        mig_policy_li = []
        with open(file_path) as f:
            for line in f:
                mig_policy = line.strip().split(",")[0]
                if mig_policy == "switch":
                    mig_policy = "SWITCH"
                elif int(mig_policy) == MIG_POLICY_LRU:
                    mig_policy = "LRU"
                elif int(mig_policy) == MIG_POLICY_LFU:
                    mig_policy = "LFU"
                elif int(mig_policy) == MIG_POLICY_PSEUDO_RANDOM:
                    mig_policy = "Random"
                mig_policy_li.append(mig_policy)

        splitted_workload_signature = workload_signature.split("_")[:-2]
        workload_signature = "_".join(splitted_workload_signature)
        result = "%s,%s" % (get_workload_nickname(workload_signature), ",".join(mig_policy_li))
        print(result)

if __name__ == "__main__":
    main()
