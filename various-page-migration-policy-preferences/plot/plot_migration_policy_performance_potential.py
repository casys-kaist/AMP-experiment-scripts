#!/usr/bin/env python3

"""
   plot_migration_policy_performance_potential.py

    Created on: Dec. 22, 2019
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

    # load data
    data = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            workload_name = splitted_line[0]
            thp = splitted_line[1]
            mig_policy = splitted_line[2]
            performance = float(splitted_line[3])

            mig_policy_thp = "%s_%s" % (mig_policy, thp)
            abbr_mig_policy_thp = abbreviate_mig_policy_thp(mig_policy_thp)
            if workload_name not in data.keys():
                data.update({workload_name:
                    {"Modified LRU Lists (b)": 0,
                     "Modified LRU Lists (h)": 0,
                     "LRU": 0,
                     "LFU": 0,
                     "Random": 0,
                     "Best": 0}})
            data[workload_name][abbr_mig_policy_thp] = performance

    # find the best performance
    for workload_name in data.keys():
        best = 0
        for policy in ["Modified LRU Lists (b)", "Modified LRU Lists (h)", "LRU", "LFU", "Random"]:
            if data[workload_name][policy] > best:
                best = data[workload_name][policy]
        data[workload_name]["Best"] = best

    # load performance
    plot_data = {"Workload Name": abbr_workload_name_li,
                 "Modified LRU Lists (b)": [], "Modified LRU Lists (h)": [], "Best": []}
    for abbr_workload_name in abbr_workload_name_li:
        plot_data["Modified LRU Lists (b)"].append(data[abbr_workload_name]["Modified LRU Lists (b)"])
        plot_data["Modified LRU Lists (h)"].append(data[abbr_workload_name]["Modified LRU Lists (h)"])
        plot_data["Best"].append(data[abbr_workload_name]["Best"])

    # geomean
    for key in plot_data.keys():
        if key != "Workload Name":
            plot_data[key].append(geomean(plot_data[key]))
    abbr_workload_name_li.append("geomean")

    # print data
    print("Evaluation")
    for key in ["Modified LRU Lists (b)", "Modified LRU Lists (h)", "Best"]:
        print(key, plot_data[key])
    print()

    # plot bar graph
    df = pd.DataFrame(plot_data)
    cmap_big = cm.get_cmap("viridis", 512)
    plot_path = "%s/migration_policy_performance_potential" % (args.result_dir)
    cmap_small = ListedColormap(cmap_big(np.linspace(0.0, 0.65, 256)))
    ax = df.plot.bar(x="Workload Name",
            y=["Modified LRU Lists (b)", "Modified LRU Lists (h)", "Best"],
            rot=80, figsize=(13, 4.4), width=0.83, cmap=cmap_small)
    ax.tick_params(axis="x", labelsize=23)
    ax.tick_params(axis="y", labelsize=21)
    ax.set_ylabel("Normalized Perf. (%)", fontsize=25.5)
    ax.yaxis.set_label_coords(-0.08, 0.40)
    ax.xaxis.label.set_visible(False)
    ax.get_legend().remove()
    ax.grid(linestyle="--", alpha=0.8)
    ax.set_ylim([0, 100.000001])
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 10))

    # shrink current axis's height by 20% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.8])

    # put a legend below current axis
    ax.legend(["Modified LRU Lists (b)", "Modified LRU Lists (h)", "Best"],
            loc="upper center", bbox_to_anchor=(0.48, -0.85),
            fontsize=23, ncol=6, columnspacing=.75)

    ax.axvline(x=10.5, color='k', linestyle="--", linewidth=2)

    # save figure
    fig = ax.get_figure()
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
