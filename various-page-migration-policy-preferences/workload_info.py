#!/usr/bin/env python3

"""
   workload_info.py

    Created on: Dec. 18, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

def get_workload_info_li(hostname):
    if hostname == "pandam01":
        workload_info_li = [
                    ["npb", "lu.D.x"], # 50-min
                    ["npb", "cg.D.x"], # 18-min
                ]
    if hostname == "pandam02":
        workload_info_li = [
                    ["speccpu2017", "605.mcf_s"], # 18-min
                    ["graph500", "graph500:bfs:23:16"], # 26-min
                    ["cloudsuite", "graph-analytics:10:1"], # 22-min
                ]
    if hostname == "pandam03":
        workload_info_li = [
                    ["speccpu2017", "603.bwaves_s"], # 20-min
                    ["cloudsuite", "in-memory-analytics:10:1"], # 19-min
                    ["speccpu2017", "628.pop2_s"], # 14-min
                ]
    if hostname == "pandam04":
        workload_info_li = [
                    ["speccpu2017", "619.lbm_s"], # 20-min
                    ["speccpu2017", "631.deepsjeng_s"], # 13-min
                    ["speccpu2017", "607.cactuBSSN_s"], # 23-min
                ]
    return workload_info_li
