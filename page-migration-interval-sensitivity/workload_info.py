#!/usr/bin/env python3

"""
   workload_info.py

    Created on: Dec. 18, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

def get_workload_info_li(hostname):
    if hostname == "pandam01":
        workload_info_li = [
                    ["npb", "lu.D.x"],
                    ["npb", "cg.D.x"],
                ]
    if hostname == "pandam02":
        workload_info_li = [
                    ["speccpu2017", "605.mcf_s"],
                    ["graph500", "graph500:bfs:23:16"],
                    ["cloudsuite", "graph-analytics:10:1"],
                ]
    if hostname == "pandam03":
        workload_info_li = [
                    ["speccpu2017", "603.bwaves_s"],
                    ["cloudsuite", "in-memory-analytics:10:1"],
                    ["speccpu2017", "628.pop2_s"],
                ]
    if hostname == "pandam04":
        workload_info_li = [
                    ["speccpu2017", "619.lbm_s"],
                    ["speccpu2017", "631.deepsjeng_s"],
                    ["speccpu2017", "607.cactuBSSN_s"],
                ]
    return workload_info_li
