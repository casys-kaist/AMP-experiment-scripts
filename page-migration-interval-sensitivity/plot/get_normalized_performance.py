#!/usr/bin/env python3

"""
   get_normalized_performance.py

    Created on: Sept. 23, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
from glob import glob
from lib.stats import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", required=True)
    args = parser.parse_args()

    data = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.split(",")
            workload_name = splitted_line[0]
            interval = splitted_line[1]
            elapsed_time = float(splitted_line[2])

            if workload_name not in data.keys():
                data.update({workload_name: {}})
            data[workload_name].update({interval: elapsed_time})

    for workload_name in data.keys():
        for interval in sorted(data[workload_name].keys()):
            print("%s,%s,%f"
                    % (workload_name, interval,
                        (data[workload_name]["2"] / data[workload_name][interval])*100))

if __name__ == "__main__":
    main()
