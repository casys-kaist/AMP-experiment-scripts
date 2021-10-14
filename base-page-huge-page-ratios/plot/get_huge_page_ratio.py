#!/usr/bin/env python3

"""
   get_huge_page_ratio.py

    Created on: Sept. 13, 2020
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


    file_path_li = glob(args.result_dir + "/*.before.meminfo.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)

        workload_signature = filename.replace(".before.meminfo.txt", "").replace("_0", "")
        workload_name = workload_signature.split(":")[0].replace("_0", "")
        abbr_workload_name = abbreviate_workload_name(workload_name)

        data = {"before": {"AnonPages": 0, "AnonHugePages": 0},
                "after": {"AnonPages": 0, "AnonHugePages": 0},
                "net": {"AnonPages": 0, "AnonHugePages": 0}}

        # before
        with open(file_path) as f:
            for line in f:
                if "AnonPages" in line:
                    splitted_line = line.strip().split()
                    val = int(splitted_line[1])
                    data["before"]["AnonPages"] = val
                if "AnonHugePages" in line:
                    splitted_line = line.strip().split()
                    val = int(splitted_line[1])
                    data["before"]["AnonHugePages"] = val

        file_path = file_path.replace("before", "after")
        with open(file_path) as f:
            for line in f:
                if "AnonPages" in line:
                    splitted_line = line.strip().split()
                    val = int(splitted_line[1])
                    data["after"]["AnonPages"] = val
                if "AnonHugePages" in line:
                    splitted_line = line.strip().split()
                    val = int(splitted_line[1])
                    data["after"]["AnonHugePages"] = val

        data["net"]["AnonPages"] = data["after"]["AnonPages"] - data["before"]["AnonPages"]
        data["net"]["AnonHugePages"] = data["after"]["AnonHugePages"] - data["before"]["AnonHugePages"]

        huge_page_ratio = data["net"]["AnonHugePages"] / data["net"]["AnonPages"]
        print("%s,%f" % (abbr_workload_name, huge_page_ratio))

if __name__ == "__main__":
    main()
