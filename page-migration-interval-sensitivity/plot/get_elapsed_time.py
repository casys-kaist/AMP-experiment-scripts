#!/usr/bin/env python3

"""
   get_elapsed_time.py

    Created on: Sept. 16, 2020
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

    data_dict = {}
    file_path_li = glob(args.result_dir + "/*.stderr.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)
        workload_signature = filename.replace(".stderr.txt", "")
        splitted_workload_signature = workload_signature.split("_")

        migration_interval = int(splitted_workload_signature[-1])
        workload_name = "_".join(splitted_workload_signature[:-4]).split(":")[0]
        workload_name = abbreviate_workload_name(workload_name)

        elapsed_seconds = 0
        with open("%s/%s" % (args.result_dir, filename)) as f:
            for line in f:
                if "elapsed" in line and "CPU" in line:
                    elapsed_seconds = time_to_seconds(line)

        print("%s,%d,%d" % (workload_name, migration_interval, elapsed_seconds))

if __name__ == "__main__":
    main()
