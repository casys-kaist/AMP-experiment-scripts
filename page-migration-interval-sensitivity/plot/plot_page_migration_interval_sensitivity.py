#!/usr/bin/env python3

"""
   plot_page_migration_interval_sensitivity.py

    Created on: Sept. 23, 2020
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
from common import *
mpl.use("Agg")
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "inherit"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", required=True)
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    cmap_big = cm.get_cmap("viridis", 512)
    cmap_small = ListedColormap(cmap_big(np.linspace(0.0, 0.65, 256)))

    data = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            workload_name = splitted_line[0]
            interval = "%d-sec" % (int(splitted_line[1]))
            performance = float(splitted_line[2])

            if workload_name not in data.keys():
                data.update({workload_name:
                    {"2-sec": 0, "3-sec": 0, "4-sec": 0, "5-sec": 0}})
            data[workload_name][interval] = performance

    plot_data = {"Workload Name": abbr_workload_name_li,
                "2-sec": [], "3-sec": [], "4-sec": [], "5-sec": []}
    for abbr_workload_name in abbr_workload_name_li:
        plot_data["2-sec"].append(data[abbr_workload_name]["2-sec"])
        plot_data["3-sec"].append(data[abbr_workload_name]["3-sec"])
        plot_data["4-sec"].append(data[abbr_workload_name]["4-sec"])
        plot_data["5-sec"].append(data[abbr_workload_name]["5-sec"])

    df = pd.DataFrame(plot_data)
    ax = df.plot.bar(x="Workload Name", y=["2-sec", "3-sec", "4-sec", "5-sec"],
            rot=80, figsize=(26, 4.4), width=0.73, cmap=cmap_small)
    ax.tick_params(axis="x", labelsize=23)
    ax.tick_params(axis="y", labelsize=23)
    ax.set_ylabel("Normalized Perf. (%)", fontsize=24)
    ax.yaxis.set_label_coords(-0.04, 0.42)
    ax.xaxis.label.set_visible(False)
    ax.get_legend().remove()
    ax.grid(linestyle="--", alpha=0.8)
    ax.set_ylim([0, 120.000001])
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 20))

    # shrink current axis's height by 20% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.8])
    ax.legend(["2-sec", "3-sec", "4-sec", "5-sec"],
            loc="upper center", bbox_to_anchor=(0.48, -1.1), fontsize=23, ncol=5, columnspacing=1.8)

    fig = ax.get_figure()
    plot_path = "%s/page_migration_interval_sensitivity" % (args.result_dir)
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
