#!/usr/bin/env python3

"""
   get_accessed_base_page_ratio.py

    Created on: Sept. 13, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
import statistics as s
from glob import glob
from lib.stats import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    file_path_li = glob(args.result_dir + "/*.memory.hotness.access_freq.accessed_base_page.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)

        workload_signature\
                = filename.replace(".memory.hotness.access_freq.accessed_base_page.txt", "")\
                .replace("_0", "")
        workload_name = workload_signature.split(":")[0].replace("_0", "")
        abbr_workload_name = abbreviate_workload_name(workload_name)

        with open(file_path) as f:
            for line in f:
                splitted_line = line.strip().split(",")
                accessed_base_page_ratio_li = [float(n)/float(512) for n in splitted_line if n != "0"]
                avg_accessed_base_page_ratio = s.mean(accessed_base_page_ratio_li)
                print("%s,%f" % (abbr_workload_name, avg_accessed_base_page_ratio))

if __name__ == "__main__":
    main()
