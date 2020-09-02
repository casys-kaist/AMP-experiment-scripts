#!/usr/bin/env python3

"""
   plot_performance.py

    Created on: Jan. 08, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import matplotlib as mpl
import matplotlib.gridspec as gridspec
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

    data_dict = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            workload_mix = splitted_line[0]
            idx = int(splitted_line[1])
            workload_name = workload_mix.split("+")[idx]
            mig_policy = splitted_line[2]
            performance = float(splitted_line[3])
            if workload_mix not in data_dict.keys():
                data_dict.update({workload_mix: {}})
            if workload_name not in data_dict[workload_mix].keys():
                data_dict[workload_mix].update({workload_name: {"LRU": None, "LFU": None, "Random": None, "AMP": None}})
            data_dict[workload_mix][workload_name][mig_policy] = performance

    index_li = []
    workload_mix_li = ["cactus+graph500", "mcf+in-mem-analytics", "cactus+deepsjeng", "mcf+lbm", "graph500+deepsjeng", "in-mem-analytics+lbm"]
    mig_policy_li = ["LRU", "LFU", "Random", "AMP"]
    for workload_mix in workload_mix_li:
        for mig_policy in mig_policy_li:
            index = "%s+%s" % (workload_mix, mig_policy)
            index_li.append(index)

    plot_data = {"Workload Mix": index_li,
                 "workload 1": [],
                 "workload 2": []}
    for workload_mix in plot_data["Workload Mix"]:
        splitted_workload_mix = workload_mix.split("+")
        workload_1_name = splitted_workload_mix[0]
        workload_2_name = splitted_workload_mix[1]
        workload_mix_name = "+".join(splitted_workload_mix[:-1])
        mig_policy = splitted_workload_mix[2]
        plot_data["workload 1"].append(data_dict[workload_mix_name][workload_1_name][mig_policy])
        plot_data["workload 2"].append(data_dict[workload_mix_name][workload_2_name][mig_policy])
    print("Multi-programmed Environment Workload Mix Perf")
    for key in ["Workload Mix", "workload 1", "workload 2"]:
        print(key, plot_data[key])
    print()

    fig = plt.figure(figsize=(26, 3.3))
    gs = gridspec.GridSpec(1, 2, width_ratios=[10, 1])
    gs.update(wspace=0.0, hspace=0)

    cmap_big = cm.get_cmap("viridis", 512)
    cmap_small = ListedColormap(cmap_big(np.linspace(0.0, 0.65, 256)))
    ax1 = plt.subplot(gs[0])
    df = pd.DataFrame(plot_data)
    df.plot.bar(ax=ax1, x="Workload Mix", y=["workload 1", "workload 2"],
            width=0.83, rot=75, cmap=cmap_small)

    ax1.axvline(x=3.5, color='k', linestyle="--", linewidth=2)
    ax1.axvline(x=7.5, color='k', linestyle="--", linewidth=2)
    ax1.axvline(x=11.5, color='k', linestyle="--", linewidth=2)
    ax1.axvline(x=15.5, color='k', linestyle="--", linewidth=2)
    ax1.axvline(x=19.5, color='k', linestyle="--", linewidth=2)

    ax1.text(-0.43, 105, "cactus+graph500", fontsize=23)
    ax1.text(3.55, 105, "mcf+in-mem-anal.", fontsize=23)
    ax1.text(7.6, 105, "cactus+deepsjeng", fontsize=23)
    ax1.text(12.6, 105, "mcf+lbm", fontsize=23)
    ax1.text(15.55, 105, "graph500+deepsj.", fontsize=23)
    ax1.text(19.6, 105, "in-mem-anal.+lbm", fontsize=23)
    ax1.text(23.92, 105, "geomean", fontsize=23)

    mig_policy_perf_dict = {"LRU": [], "LFU": [], "Random": [], "AMP": []}
    for workload_mix in data_dict.keys():
        for workload_name in data_dict[workload_mix].keys():
            for mig_policy in data_dict[workload_mix][workload_name].keys():
                perf = data_dict[workload_mix][workload_name][mig_policy]
                mig_policy_perf_dict[mig_policy].append(perf)
    perf_li = []
    for mig_policy in mig_policy_li:
        perf_li.append(geomean(mig_policy_perf_dict[mig_policy]))

    print("Multi-programmed Environment Geomean")
    print(mig_policy_li)
    print(perf_li)
    print()

    ax2 = plt.subplot(gs[1])
    plot_data = {"Workload Mix": mig_policy_li, "Performance": perf_li}
    df = pd.DataFrame(plot_data)
    df.plot.bar(ax=ax2, x="Workload Mix", y=["Performance"], width=0.83, rot=75, cmap=cmap_small)
    for ax in [ax1, ax2]:
        ax.tick_params(axis="x", labelsize=23)
        ax.tick_params(axis="y", labelsize=22)
        if ax == ax1:
            ax.set_ylabel("Normalized Perf. (%)", fontsize=24)
        else:
            ax.set_ylabel("")
        ax.yaxis.set_label_coords(-0.040, 0.41)
        ax.xaxis.label.set_visible(False)
        ax.get_legend().remove()
        ax.grid(linestyle="--", alpha=0.8)
        ax.set_ylim([0, 100.0000001])
        start, end = ax.get_ylim()
        ax.yaxis.set_ticks(np.arange(start, end, 20))
        ax.set_xticklabels(mig_policy_li*6)
    ax2.yaxis.set_ticklabels([])

    plot_path = "%s/migration_policy_performance_evaluation_multi_programmed" % (args.result_dir)
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
