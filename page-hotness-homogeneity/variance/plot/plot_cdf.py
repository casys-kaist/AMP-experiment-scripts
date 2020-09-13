#!/usr/bin/env python3

"""
   plot_cdf.py

    Created on: Sept. 13, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
plt.rcParams["legend.fancybox"] = False
plt.rcParams["legend.edgecolor"] = "inherit"

def cdf(data):
    n = len(data)
    x = np.sort(data)
    y = np.arange(1, n + 1) / n
    return x, y

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", required=True)
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    with open(args.data) as f:
        lines = f.readlines()
        for line in lines:
            fig, ax = plt.subplots(figsize=(5, 5))

            workload_name = line.split(",")[0]
            stdev_li = list(map(float, line.split(",")[1:]))
            x_data, y_data = cdf(stdev_li)
            ax.plot(x_data, y_data, linewidth=2.5, color="k", linestyle="-")

            ax.set_title(workload_name, fontsize=16)
            ax.set_ylabel("Probability", fontsize=16)
            ax.set_xlabel("STDEV", fontsize=16)
            ax.xaxis.set_tick_params(labelsize=15)
            ax.yaxis.set_tick_params(labelsize=15)
            ax.set_xticks(np.arange(0, 8.00001, 1))
            ax.set_yticks(np.arange(0, 1.00001, 0.1))
            ax.grid(linestyle="--", alpha=0.8)
            path = "%s/%s" % (args.result_dir, workload_name.replace(".", "_"))
            fig.savefig(path + ".png", bbox_inches="tight")
            fig.savefig(path + ".pdf", bbox_inches="tight")
            plt.close()

if __name__ == "__main__":
    main()
