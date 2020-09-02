#!/usr/bin/env python3

"""
   workload_mix.py

    Created on: Jan. 08, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

workload_mix_li = [
            [["speccpu2017", "605.mcf_s"], ["cloudsuite", "in-memory-analytics:10:1"]], # LRU + LFU
            [["speccpu2017", "607.cactuBSSN_s"], ["graph500", "graph500:bfs:23:16"]], # LRU + LFU
            [["speccpu2017", "605.mcf_s"], ["speccpu2017", "619.lbm_s"]], # LRU + Random
            [["speccpu2017", "607.cactuBSSN_s"], ["speccpu2017", "631.deepsjeng_s"]], # LRU + Random
            [["cloudsuite", "in-memory-analytics:10:1"], ["speccpu2017", "619.lbm_s"]], # LFU + Random
            [["graph500", "graph500:bfs:23:16"], ["speccpu2017", "631.deepsjeng_s"]], # LFU + Random
        ]
