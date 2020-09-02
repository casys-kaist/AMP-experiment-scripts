#!/usr/bin/env python3

"""
   common.py

    Created on: Sep. 12, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

def get_workload_nickname(workload_signature):
    workload_signature_workload_name_dict = {
                "mix+lru_favor:512000:4:20:193594924+lfu_favor:51200:0.5:401427297": "Mix 1",
                "mix+lfu_favor:51200:0.5:401427297+lru_favor:512000:4:20:193594924": "Mix 2",
                "mix+lru_favor:512000:4:20:193594924+random_favor:131072:105236354": "Mix 3",
                "mix+lfu_favor:51200:0.5:401427297+random_favor:131072:105236354": "Mix 4",
                "mix+random_favor:131072:105236354+lru_favor:512000:4:20:193594924": "Mix 5",
                "mix+random_favor:131072:105236354+lfu_favor:51200:0.5:401427297": "Mix 6",
            }
    return workload_signature_workload_name_dict[workload_signature]
