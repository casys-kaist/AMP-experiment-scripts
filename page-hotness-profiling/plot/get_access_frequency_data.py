#!/usr/bin/env python3

"""
   get_access_frequency_data.py

    Created on: Apr. 16, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
from glob import glob

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    file_path_li = glob(args.result_dir + "/*.memory.hotness.access_freq.stats.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)

        mat = []
        with open(file_path) as f:
            for line in f:
                splitted_line = line.strip().split(",")
                mat.append([float(n) for n in splitted_line[1:]])
        mat = list(map(list, zip(*mat)))

        file_path = file_path.replace(".txt", ".transpose.txt")
        with open(file_path, "w") as f:
            for line in mat:
                f.write(",".join(map(str, line)) + "\n")

if __name__ == "__main__":
    main()
