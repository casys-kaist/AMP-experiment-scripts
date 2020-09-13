#!/usr/bin/env python3

"""
   workload_info.py

    Created on: Sept. 13, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

def get_workload_info_li(hostname):
    if hostname == "pandam01":
        workload_info_li = [
                    ["npb", "lu.D.x", 300],
                    ["npb", "cg.D.x", 300],
                ]
    if hostname == "pandam02":
        workload_info_li = [
                    ["speccpu2017", "605.mcf_s", 300],
                    ["graph500", "graph500:bfs:23:16", 300],
                    ["cloudsuite", "graph-analytics:10:1", 300],
                ]
    if hostname == "pandam03":
        workload_info_li = [
                    ["speccpu2017", "603.bwaves_s", 300],
                    ["cloudsuite", "in-memory-analytics:10:1", 300],
                    ["speccpu2017", "628.pop2_s", 300],
                ]
    if hostname == "pandam04":
        workload_info_li = [
                    ["speccpu2017", "619.lbm_s", 300],
                    ["speccpu2017", "631.deepsjeng_s", 300],
                    ["speccpu2017", "607.cactuBSSN_s", 300],
                ]
    return workload_info_li
