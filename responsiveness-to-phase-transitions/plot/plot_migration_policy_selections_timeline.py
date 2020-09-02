#!/usr/bin/env python3

"""
   plot_migration_policy_selections_timeline.py

    Created on: Jul. 22, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.lines import Line2D
from common import *
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "inherit"

workload_nickname_li = [ "Mix 1", "Mix 2", "Mix 3", "Mix 4", "Mix 5", "Mix 6" ]
mig_policy_set = [ "Random", "LFU", "LRU" ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-result_dir", required=True)
    parser.add_argument("-data", required=True)
    parser.add_argument("-n_rows", default=2)
    parser.add_argument("-n_cols", default=3)
    args = parser.parse_args()

    data = {}
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            workload_nickname = splitted_line[0]
            mig_policy_li = splitted_line[1:]
            data.update({workload_nickname: mig_policy_li})

    fig, axs = plt.subplots(args.n_rows, args.n_cols)
    axs = axs.flatten()
    fig.set_size_inches(11, 2.8)
    plt.subplots_adjust(left=0.04, right=0.65, bottom=0.05, top=0.65, wspace=0.1, hspace=1.2)

    marker_set = [ "s", "D", "o" ]
    colors = []
    cmap = cm.get_cmap("gnuplot")
    for i in range(3):
        colors.append(cmap(i*0.333))
    tmp = colors[1]
    colors[1] = colors[0]
    colors[0] = tmp

    for i in range(args.n_rows * args.n_cols):
        workload_nickname = workload_nickname_li[i]
        mig_policy_li = data[workload_nickname]
        mig_policy_li = list(filter(("SWITCH").__ne__, mig_policy_li))
        ax = axs[i]
        for i, mig_policy in enumerate(mig_policy_li):
            x = i
            y = mig_policy_set.index(mig_policy) + 1
            ax.scatter(np.reshape(x, -1), np.reshape(y, -1),
                    c=[list(reversed(colors))[y-1]], marker=list(reversed(marker_set))[y-1], s=40)
        ax.set_title(workload_nickname, fontsize=15)
        ax.tick_params(axis="x", labelsize=15)
        ax.tick_params(axis="y", labelsize=15)
        ax.set_yticks(np.arange(1, len(mig_policy_set)+1, 1))
        ax.axes.get_yaxis().set_visible(False)
        ax.set_ylim(0.7, 3.3)

        mig_policy_li = data[workload_nickname]
        idx = mig_policy_li.index("SWITCH") - 1
        ax.axvline(x=idx, color='k', linestyle="--", linewidth=2)

    fig.text(0.015, 0.15, "Policy", va="center", rotation="vertical", fontsize=15)
    fig.text(0.015, 0.56, "Policy", va="center", rotation="vertical", fontsize=15)
    fig.text(0.345, -0.13, "Epochs", ha="center", fontsize=15)
    legend_elements = [
        Line2D([0], [0], marker="s", color="w", label="LRU", markerfacecolor=colors[0], markersize=13),
        Line2D([0], [0], marker="D", color="w", label="LFU", markerfacecolor=colors[1], markersize=13),
        Line2D([0], [0], marker="o", color="w", label="Random", markerfacecolor=colors[2], markersize=13),
    ]
    ax.legend(handles=legend_elements, bbox_to_anchor=(-0.63, -2.2), loc="lower center", ncol=4, fontsize=15)

    plot_path = "%s/responsiveness_to_phase_transitions" % (args.result_dir)
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()
