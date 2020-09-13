#!/usr/bin/env python3

"""
   plot_access_frequency.py

    Created on: Apr. 16, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
from glob import glob
from lib.stats import *
mpl.use("Agg")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    file_path_li = glob(args.result_dir + "/*.memory.hotness.access_freq.stats.transpose.txt")
    for file_path in file_path_li:
        path, filename = os.path.split(file_path)

        workload_signature\
                = filename.replace(".memory.hotness.access_freq.stats.transpose.txt", "")\
                .replace("_0", "")
        scanning_interval = int(workload_signature.split("_")[-1])
        thp = workload_signature.split("_")[-2]
        if thp == "always":
            thp = "2MB"
        else:
            thp = "4KB"
        workload_signature = "_".join(workload_signature.split("_")[:-2])
        workload_name = workload_signature.split(":")[0].replace("_0", "")
        abbr_workload_name = abbreviate_workload_name(workload_name)

        y_values = []
        with open(file_path) as f:
            for line in f:
                splitted_line = line.split(",")
                value_li = [float(n) / 1024 / 1024 for n in splitted_line]
                y_values.append(value_li)
        y_values = list(reversed(y_values))
        x_values = range(len(y_values[-1]))

        fig, ax = plt.subplots()
        fig.set_size_inches(6, 2)
        fig.tight_layout()
        pal = sns.light_palette("darkred", n_colors=len(y_values), reverse=True)
        ax.stackplot(x_values, y_values, colors=pal)
        ax.set_xlabel("Execution Time (epochs)", fontsize=15)
        ax.set_xlim(min(x_values), max(x_values))
        ax.set_ylim(bottom=0)
        start, end = ax.get_ylim()
        ax.tick_params(axis="x", labelsize=15)
        ax.tick_params(axis="y", labelsize=15)
        ax.set_ylabel("Allocated\nMem. Size (MB)", fontsize=15)
        ax.set_title("%s - %s %ds" % (abbr_workload_name, thp, scanning_interval), fontsize=16.5)
        tick_interval = int(end / 5)
        ax.yaxis.set_ticks(np.arange(start, end, tick_interval))

        line_plot_data = [0] * len(y_values[0])
        for y_value_li in y_values:
            for i in range(len(y_values[0])):
                line_plot_data[i] += y_value_li[i]
        ax.plot(x_values, line_plot_data, linewidth=1.7, color="black")

        print(abbr_workload_name)
        filename = "%s_%s_%d" % (abbr_workload_name.replace(".", "_"), thp, scanning_interval)
        filename = filename.replace("_.", ".").replace("__", "_")
        plot_path = "%s/%s" % (args.result_dir, filename)
        fig.savefig(plot_path + ".png", bbox_inches="tight")
        fig.savefig(plot_path + ".pdf", bbox_inches="tight")
        plt.close()

if __name__ == "__main__":
    main()
