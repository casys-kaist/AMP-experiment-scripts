#!/usr/bin/env python3

"""
   workload_info.py

    Created on: Sep. 5, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

def get_workload_info_li(hostname):
    if hostname == "rabbit01":
        workload_info_li = [
                ["cloudsuite", "graph-analytics:10:1"],
            ]
    elif hostname == "rabbit02":
        workload_info_li = [
                ["cloudsuite", "in-memory-analytics:10:1"],
            ]
    elif hostname == "rabbit03":
        workload_info_li = [
                ["graph500", "graph500:bfs:23:16"],
            ]
    elif hostname == "rabbit04":
        workload_info_li = [
                ["npb", "cg.D.x"],
            ]
    elif hostname == "rabbit05":
        workload_info_li = [
                ["npb", "lu.D.x"],
            ]
    elif hostname == "rabbit06":
        workload_info_li = [
                ["speccpu2017", "628.pop2_s"],
            ]
    elif hostname == "rabbit07":
        workload_info_li = [
                ["speccpu2017", "603.bwaves_s"],
            ]
    elif hostname == "rabbit08":
        workload_info_li = [
                ["speccpu2017", "605.mcf_s"],
            ]
    elif hostname == "rabbit09":
        workload_info_li = [
                ["speccpu2017", "607.cactuBSSN_s"],
            ]
    elif hostname == "rabbit10":
        workload_info_li = [
                ["speccpu2017", "619.lbm_s"],
            ]
    elif hostname == "rabbit11":
        workload_info_li = [
                ["speccpu2017", "631.deepsjeng_s"],
            ]
    return workload_info_li
