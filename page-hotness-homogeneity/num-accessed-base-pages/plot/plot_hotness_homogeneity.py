#!/usr/bin/env python3

"""
   plot_hotness_homogeneity.py

    Created on: Sept. 21, 2020
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

abbr_workload_name_li = [
    "mcf", "cactus", "cg.D.x",
    "graph-analytics", "in-mem-analytics", "graph500", "pop2",
    "deepsjeng", "lbm", "lu.D.x",
    "bwaves",
]

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
            huge_page_access_ratio = float(splitted_line[1]) * 100
            data[workload_name] = huge_page_access_ratio

    # load performance
    plot_data = {"Workload Name": abbr_workload_name_li,
                 "Huge Page Access Ratio": []}
    for abbr_workload_name in abbr_workload_name_li:
        plot_data["Huge Page Access Ratio"].append(data[abbr_workload_name])

    # geomean
    for key in plot_data.keys():
        if key != "Workload Name":
            plot_data[key].append(geomean(plot_data[key]))
    abbr_workload_name_li.append("geomean")

    # print data
    print("Ideal")
    for key in ["Huge Page Access Ratio"]:
        print(key, plot_data[key])
    print()

    # plot bar graph
    df = pd.DataFrame(plot_data)
    cmap_big = cm.get_cmap("gray", 512)
    plot_path = "%s/huge_page_access_ratio" % (args.result_dir)
    cmap_small = ListedColormap(cmap_big(np.linspace(0.0, 0.65, 256)))
    ax = df.plot.bar(x="Workload Name",
            y=["Huge Page Access Ratio"],
            rot=80, figsize=(13, 3.8), width=0.83, cmap=cmap_small)
    ax.tick_params(axis="x", labelsize=23)
    ax.tick_params(axis="y", labelsize=23)
    ax.set_ylabel("Huge Page Acc. Ratio (%)", fontsize=25.5)
    ax.yaxis.set_label_coords(-0.08, 0.33)
    ax.xaxis.label.set_visible(False)
    ax.get_legend().remove()
    ax.grid(linestyle="--", alpha=0.8)
    ax.set_ylim([0, 100.000001])
    start, end = ax.get_ylim()
    ax.yaxis.set_ticks(np.arange(start, end, 10))

    ax.axvline(x=10.5, color='k', linestyle="--", linewidth=2)

    # save figure
    fig = ax.get_figure()
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
