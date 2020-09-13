#!/usr/bin/env python3

"""
   get_stdev_li.py

    Created on: Sept. 13, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
import math
from glob import glob
from lib.stats import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    file_path_li = glob(args.result_dir + "/*.memory.hotness.access_freq.variance.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)

        workload_signature\
                = filename.replace(".memory.hotness.access_freq.variance.txt", "")\
                .replace("_0", "")
        workload_name = workload_signature.split(":")[0].replace("_0", "")
        abbr_workload_name = abbreviate_workload_name(workload_name)

        stdev_li = []
        with open(file_path) as f:
            for line in f:
                splitted_line = line.strip().split(",")
                stdev_li = [math.sqrt(float(n)) for n in splitted_line]
                print("%s,%s" % (abbr_workload_name, ",".join(map(str, stdev_li))))

if __name__ == "__main__":
    main()
