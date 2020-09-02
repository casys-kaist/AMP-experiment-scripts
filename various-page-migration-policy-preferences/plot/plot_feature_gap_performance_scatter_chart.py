#!/usr/bin/env python3

"""
   plot_feature_gap_performance_scatter_chart.py

    Created on: Dec. 18, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
mpl.use("Agg")
mpl.rcParams["legend.fancybox"] = False
mpl.rcParams["legend.edgecolor"] = "inherit"
plt.style.use("grayscale")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", required=True)
    parser.add_argument("-result_dir", required=True)
    args = parser.parse_args()

    # load data
    x_pos_li = []
    y_pos_li = []
    with open(args.data) as f:
        for line in f:
            splitted_line = line.strip().split(",")
            abbr_workload_name = splitted_line[0]
            thp = splitted_line[1]
            if thp == "always":
                mig_policy = splitted_line[2]
                feature_name = splitted_line[3]
                feature_value_gap = float(splitted_line[4])
                perf = float(splitted_line[5])
                x_pos_li.append(feature_value_gap)
                y_pos_li.append(perf)

    # plot
    fig, ax = plt.subplots()
    fig.set_size_inches(4.5, 2.5)
    fig.tight_layout()
    plt.scatter(x_pos_li, y_pos_li, s=30)
    ax.set_xlabel("Feature Value Gap", fontsize=17.5)
    ax.set_ylabel("Normalized\nPerformance (%)", fontsize=17.5)
    ax.tick_params(axis="x", labelsize=15)
    ax.tick_params(axis="y", labelsize=15)
    ax.set_title(feature_name, fontsize=18)

    xaxis_min = -0.1
    xaxis_max = 1.00000001
    xaxis_interval = 0.1
    yaxis_min = 35
    yaxis_max = 105.000001
    yaxis_interval = 10
    ax.set_xlim((xaxis_min, xaxis_max))
    ax.set_ylim((yaxis_min, yaxis_max))
    ax.xaxis.set_ticks(np.arange(xaxis_min, xaxis_max, xaxis_interval))
    ax.yaxis.set_ticks(np.arange(yaxis_min, yaxis_max, yaxis_interval))
    ax.xaxis.set_label_coords(0.5, -0.3)
    ax.grid(linestyle="--", alpha=0.5)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=70)
    plot_path = "%s/feature_gap_normalized_perf_correlation_%s"\
            % (args.result_dir, feature_name.replace(" ", "_").lower())
    fig.savefig(plot_path + ".png", bbox_inches="tight")
    fig.savefig(plot_path + ".pdf", bbox_inches="tight")
    plt.close()

    print(feature_name, pearsonr(x_pos_li, y_pos_li))

if __name__ == "__main__":
    main()

