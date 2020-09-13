#!/usr/bin/env python3

"""
   get_uniq_lines.py

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

    file_path_li = glob(args.result_dir + "/*.hotness.*.stats.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)

        cmd = "uniq %s > /tmp/%s" % (file_path, filename)
        os.system(cmd)

        cmd = "mv /tmp/%s %s" % (filename, file_path)
        os.system(cmd)

if __name__ == "__main__":
    main()
