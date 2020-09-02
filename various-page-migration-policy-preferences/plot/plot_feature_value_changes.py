#!/usr/bin/env python3

"""
   plot_feature_value_changes.py

    Created on: Dec. 25, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import itertools
import matplotlib as mpl
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
mpl.use("Agg")
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "inherit"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", required=True)
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    # get feature name
    feature_name = args.data.split("/")[-1].replace(".txt", "")

    # load data
    data = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            abbr_workload_name = splitted_line[0]
            mig_policy = splitted_line[2]
            feature_values_li = list(map(float, splitted_line[3:]))

            if abbr_workload_name not in data.keys():
                data.update({abbr_workload_name: {}})
            if ("Modified" not in mig_policy) and ("Random" not in mig_policy):
                data[abbr_workload_name].update({mig_policy: feature_values_li})

    # prepare colors
    colors = []
    cmap = cm.get_cmap("gnuplot")
    for i in range(3):
        colors.append(cmap(i*0.333))
    colors = colors[:-1]

    # plot
    for abbr_workload_name in data.keys():
        fig = plt.figure(figsize=(9.0, 2.4))
        gs = gridspec.GridSpec(1, 1)
        ax = plt.subplot(gs[0])
        ax.set_title("%s - %s" % (abbr_workload_name, " ".join(feature_name.split("_")).title()), fontsize=19)
        ax.set_xlabel("Epochs", fontsize=18)
        ax.set_ylabel("Feature Value", fontsize=18)
        ax.tick_params(axis="x", labelsize=17)
        ax.tick_params(axis="y", labelsize=17)
        ax.set_ylim(0, 100.00001)
        start, end = ax.get_ylim()
        ax.yaxis.set_ticks(np.arange(start, end, 20))
        ax.grid(linestyle="--", alpha=0.8)

        marker_li = itertools.cycle(("D", "s"))
        ls_li = itertools.cycle(("-", "--"))
        color_li = itertools.cycle(colors)
        for idx, mig_policy in enumerate(sorted(data[abbr_workload_name].keys())):
            feature_values_li = data[abbr_workload_name][mig_policy]
            color = next(color_li)
            ax.plot(feature_values_li, linewidth=3, color=color,
                    marker=next(marker_li), markersize=12, markerfacecolor=color, markevery=35,
                    linestyle=next(ls_li),
                    label=mig_policy)

        # add legend
        handles, labels = ax.get_legend_handles_labels()
        handles = list(reversed(handles))
        labels = list(reversed(labels))
        ax.legend(handles, labels, bbox_to_anchor=(0.5, -0.75),
                loc='lower center', ncol=5, fontsize=18, markerscale=1.1)

        filename = "%s_%s" % (abbr_workload_name, feature_name)
        filename = filename.replace(" ", "_").replace(".", "_").replace("__", "_")
        plot_path = "%s/%s" % (args.result_dir, filename)
        fig.savefig(plot_path + ".png", bbox_inches="tight")
        fig.savefig(plot_path + ".pdf", bbox_inches="tight")
        plt.close()

if __name__ == "__main__":
    main()
