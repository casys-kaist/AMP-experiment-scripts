#!/usr/bin/env python3

"""
   plot_fast_memory_ratio_sensitivity.py

    Created on: June. 14, 2021
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib.colors import ListedColormap
from lib.stats import *
mpl.use("Agg")
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "inherit"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", required=True)
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    cmap_big = cm.get_cmap("viridis", 512)
    cmap_small = ListedColormap(cmap_big(np.linspace(0.0, 0.80, 256)))

    data = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            fast_memory_ratio = splitted_line[0]
            conf = splitted_line[1]
            performance = float(splitted_line[2])

            if fast_memory_ratio not in data.keys():
                data.update({fast_memory_ratio:
                    {"Mod. LRU Lists (b)": 0, "Mod. LRU Lists (h)": 0, "LRU": 0, "LFU": 0, "Random": 0, "AMP": 0}})
            data[fast_memory_ratio][conf] = performance

    plot_data = {"Conf Name": ["30%", "50%", "70%"],
                 "Mod. LRU Lists (b)": [], "Mod. LRU Lists (h)": [], "LRU": [], "LFU": [], "Random": [], "AMP": []}
    for fast_memory_ratio in ["30%", "50%", "70%"]:
        plot_data["Mod. LRU Lists (b)"].append(data[fast_memory_ratio]["Mod. LRU Lists (b)"])
        plot_data["Mod. LRU Lists (h)"].append(data[fast_memory_ratio]["Mod. LRU Lists (h)"])
        plot_data["LRU"].append(data[fast_memory_ratio]["LRU"])
        plot_data["LFU"].append(data[fast_memory_ratio]["LFU"])
        plot_data["Random"].append(data[fast_memory_ratio]["Random"])
        plot_data["AMP"].append(data[fast_memory_ratio]["AMP"])

    df = pd.DataFrame(plot_data)
    ax = df.plot.bar(x="Conf Name", y=["Mod. LRU Lists (b)", "Mod. LRU Lists (h)", "LRU", "LFU", "Random", "AMP"],
            rot=0, figsize=(17, 6), width=0.73, cmap=cmap_small)
    ax.tick_params(axis="x", labelsize=23)
    ax.tick_params(axis="y", labelsize=23)
    ax.set_ylabel("Normalized Perf. (%)", fontsize=24)
    ax.xaxis.label.set_visible(False)
    ax.get_legend().remove()
    ax.grid(linestyle="--", alpha=0.8)
    ax.set_ylim([0, 100.000001])
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 20))

    # shrink current axis's height by 20% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.8])
    ax.legend(["Mod. LRU Lists (b)", "Mod. LRU Lists (h)", "LRU", "LFU", "Random", "AMP"],
            loc="upper center", bbox_to_anchor=(0.5, -0.2), fontsize=23, ncol=5, columnspacing=1.8)

    fig = ax.get_figure()
    plot_path = "%s/page_migration_fast_memory_ratio_sensitivity" % (args.result_dir)
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
