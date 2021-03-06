#!/usr/bin/env python3

"""
   get_page_migration_stability_avg.py

    Created on: Dec. 27, 2019
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
    file_path_li = glob(args.result_dir + "/*.stderr.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)
        workload_signature = filename.replace(".stderr.txt", "")
        if ("no-migration" not in workload_signature)\
                and ("amp" not in workload_signature):
            fast_memory_ratio, thp, mig_policy, abbr_workload_name\
                    = parse_workload_signature(workload_signature)

            num_total_pages_li = []
            num_page_migrations_li = []
            file_path = "%s/%s_0.memory.migration.stats.num_total_pages.txt"\
                    % (args.result_dir, workload_signature)
            with open(file_path) as f:
                for line in f:
                    num_total_pages_li.append(int(line.strip()))

            file_path = "%s/%s_0.memory.migration.stats.num_page_migrations.txt"\
                    % (args.result_dir, workload_signature)
            with open(file_path) as f:
                for line in f:
                    num_page_migrations_li.append(int(line.strip()))

            num_total_pages = sum(num_total_pages_li)
            num_page_migrations = sum(num_page_migrations_li)
            page_migration_stability = ((num_total_pages-num_page_migrations) * 100) / num_total_pages

            if abbr_workload_name not in data_dict.keys():
                data_dict.update({abbr_workload_name: {"always": {}, "never": {}}})
            data_dict[abbr_workload_name][thp].update({mig_policy: page_migration_stability})

    for abbr_workload_name in data_dict.keys():
        for thp in data_dict[abbr_workload_name].keys():
            for mig_policy in data_dict[abbr_workload_name][thp].keys():
                page_migration_stability = data_dict[abbr_workload_name][thp][mig_policy]
                result = "%s,%s,%s,%f" % (abbr_workload_name, thp, mig_policy, page_migration_stability)
                print(result)

if __name__ == "__main__":
    main()
