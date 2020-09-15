#!/usr/bin/env python3

"""
   common.py

    Created on: Jan. 08, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

abbr_workload_name_li = [
    "mcf", "cactus", "cg.D.x",
    "graph-analytics", "in-mem-analytics", "graph500", "pop2",
    "deepsjeng", "lbm", "lu.D.x",
    "bwaves",
]

def refine_workload_name(workload_name):
    if ":" in workload_name:
        workload_name = workload_name.split(":")[0]
    workload_name = workload_name.replace("_0", "")
    return workload_name
