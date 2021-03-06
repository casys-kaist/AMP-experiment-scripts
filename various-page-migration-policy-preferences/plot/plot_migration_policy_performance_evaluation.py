#!/usr/bin/env python3

"""
   plot_migration_policy_performance_evaluation.py

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

    cmap_big = cm.get_cmap("viridis", 512)
    cmap_small = ListedColormap(cmap_big(np.linspace(0.0, 0.65, 256)))

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
                     "AMP": 0}})
            data[workload_name][abbr_mig_policy_thp] = performance

    plot_data = {"Workload Name": abbr_workload_name_li,
                 "Modified LRU Lists (b)": [],
                 "Modified LRU Lists (h)": [],
                 "LRU": [],
                 "LFU": [],
                 "Random": [],
                 "AMP": []}
    for abbr_workload_name in abbr_workload_name_li:
        plot_data["Modified LRU Lists (b)"].append(data[abbr_workload_name]["Modified LRU Lists (b)"])
        plot_data["Modified LRU Lists (h)"].append(data[abbr_workload_name]["Modified LRU Lists (h)"])
        plot_data["LRU"].append(data[abbr_workload_name]["LRU"])
        plot_data["LFU"].append(data[abbr_workload_name]["LFU"])
        plot_data["Random"].append(data[abbr_workload_name]["Random"])
        plot_data["AMP"].append(data[abbr_workload_name]["AMP"])

    for key in plot_data.keys():
        if key != "Workload Name":
            plot_data[key].append(geomean(plot_data[key]))
    abbr_workload_name_li.append("geomean")

    print("Evaluation")
    for key in ["Modified LRU Lists (b)", "Modified LRU Lists (h)", "LRU", "LFU", "Random", "AMP"]:
        print(key, plot_data[key])
    print()

    df = pd.DataFrame(plot_data)
    ax = df.plot.bar(x="Workload Name",
            y=["Modified LRU Lists (b)", "Modified LRU Lists (h)", "LRU", "LFU", "Random", "AMP"],
            rot=80, figsize=(26, 4.4), width=0.83, cmap=cmap_small)
    ax.tick_params(axis="x", labelsize=23)
    ax.tick_params(axis="y", labelsize=21)
    ax.set_ylabel("Normalized Perf. (%)", fontsize=25.5)
    ax.yaxis.set_label_coords(-0.035, 0.40)
    ax.xaxis.label.set_visible(False)
    ax.get_legend().remove()
    ax.grid(linestyle="--", alpha=0.8)
    ax.set_ylim([0, 100.000001])
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 10))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
    ax.legend(["Modified LRU Lists (b)", "Modified LRU Lists (h)", "LRU", "LFU", "Random", "AMP"],
            loc="upper center", bbox_to_anchor=(0.48, -1.1),
            fontsize=23, ncol=6, columnspacing=.75)

    ax.axvline(x=2.5, color='k', linestyle="--", linewidth=2)
    ax.axvline(x=6.5, color='k', linestyle="--", linewidth=2)
    ax.axvline(x=9.5, color='k', linestyle="--", linewidth=2)
    ax.axvline(x=10.5, color='k', linestyle="--", linewidth=2)

    ax.text(0.5, 105, "LRU-favor", fontsize=23)
    ax.text(4.05, 105, "LFU-favor", fontsize=23)
    ax.text(7.4, 105, "Random-favor", fontsize=23)
    ax.text(9.65, 105, "Neutral", fontsize=23)

    plot_path = "%s/migration_policy_performance_evaluation" % (args.result_dir)
    fig = ax.get_figure()
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
