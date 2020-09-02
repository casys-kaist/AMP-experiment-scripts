#!/usr/bin/env python3

"""
   plot_migration_policy_selections_timeline.py

    Created on: Dec. 26, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from lib.stats import *
from common import *
mpl.use("Agg")
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "inherit"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    parser.add_argument("-data", required=True)
    args = parser.parse_args()

    # find available arms
    mig_policy_set = [ MIG_POLICY_PSEUDO_RANDOM, MIG_POLICY_LFU, MIG_POLICY_LRU ]
    mig_policy_labels = [ "Random", "LFU", "LRU" ]

    # load data
    data_dict = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            abbr_workload_name = splitted_line[0]
            mig_policy_li = list(map(int, splitted_line[1:]))
            data_dict.update({abbr_workload_name: mig_policy_li})

    # prepare colors
    marker_set = [ "s", "D", "o" ]
    colors = []
    cmap = cm.get_cmap("gnuplot")
    for i in range(3):
        colors.append(cmap(i*0.333))
    tmp = colors[1]
    colors[1] = colors[0]
    colors[0] = tmp

    # plot arms
    for abbr_workload_name in data_dict.keys():
        mig_policy_li = data_dict[abbr_workload_name]
        fig, ax = plt.subplots()
        fig.set_size_inches(9, 2.5)
        fig.tight_layout()
        ax.set_title(abbr_workload_name, fontsize=20)
        ax.set_xlabel("Epochs", fontsize=20)
        ax.tick_params(axis="x", labelsize=17)
        ax.tick_params(axis="y", labelsize=17)
        ax.set_yticklabels(mig_policy_labels)
        for i, mig_policy in enumerate(mig_policy_li):
            x = i
            y = mig_policy_set.index(mig_policy) + 1 # index starting from zero
            ax.scatter(np.reshape(x, -1), np.reshape(y, -1),
                    c=[list(reversed(colors))[y-1]],
                    marker=list(reversed(marker_set))[y-1], s=60)
        ticks = np.arange(0, len(mig_policy_set) - 0.1, 1)
        ax.set_yticks(np.arange(1, len(mig_policy_set) + 1, 1))
        ax.set_ylim(0.9, 3.1)

        legend_elements = [
            Line2D([0], [0], marker="s", color="w", label="LRU", markerfacecolor=colors[0], markersize=13),
            Line2D([0], [0], marker="D", color="w", label="LFU", markerfacecolor=colors[1], markersize=13),
            Line2D([0], [0], marker="o", color="w", label="Random", markerfacecolor=colors[2], markersize=13),
        ]
        ax.legend(handles=legend_elements, bbox_to_anchor=(0.5, -0.7), loc="lower center", ncol=4, fontsize=18)

        plot_path = "%s/%s_mig_policy_selection_timeline"\
                % (args.result_dir, abbr_workload_name.replace(":", "_"))
        fig.savefig(plot_path + ".png", bbox_inches="tight")
        fig.savefig(plot_path + ".pdf", bbox_inches="tight")
        plt.close(fig)

if __name__ == "__main__":
    main()
