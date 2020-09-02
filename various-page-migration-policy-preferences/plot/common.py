#!/usr/bin/env python3

"""
   common.py

    Created on: Dec. 22, 2019
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

from itertools import islice
from lib.stats import *

MIG_POLICY_NOP = 0
MIG_POLICY_PURE_RANDOM = 1
MIG_POLICY_PSEUDO_RANDOM = 2
MIG_POLICY_MODIFIED_LRU_LISTS = 3
MIG_POLICY_LRU = 4
MIG_POLICY_LFU = 5

abbr_workload_name_li = [
    "mcf", "cactus", "cg.D.x",
    "graph-analytics", "in-mem-analytics", "graph500", "pop2",
    "deepsjeng", "lbm", "lu.D.x",
    "bwaves",
]

def refine_migration_policy(migration_policy):
    if migration_policy == "no-migration":
        return "No Migration"
    if migration_policy == "random":
        return "Random"
    if migration_policy == "modified-lru-lists":
        return "Modified LRU Lists"
    if migration_policy == "lru":
        return "LRU"
    if migration_policy == "lfu":
        return "LFU"
    if migration_policy == "amp":
        return "AMP"

def get_mig_policy_str(mig_policy):
    if mig_policy == MIG_POLICY_LRU:
        return "LRU"
    if mig_policy == MIG_POLICY_LFU:
        return "LFU"
    if mig_policy == MIG_POLICY_PSEUDO_RANDOM:
        return "Random"

def abbreviate_mig_policy_thp(mig_policy_thp):
    if mig_policy_thp == "Modified LRU Lists_never":
        return "Modified LRU Lists (b)"
    if mig_policy_thp == "Modified LRU Lists_always":
        return "Modified LRU Lists (h)"
    if mig_policy_thp == "LRU_always":
        return "LRU"
    if mig_policy_thp == "LFU_always":
        return "LFU"
    if mig_policy_thp == "Random_always":
        return "Random"
    if mig_policy_thp == "AMP_always":
        return "AMP"
    if mig_policy_thp == "Ideal_always":
        return "Ideal"

def refine_workload_name(workload_name):
    if ":" in workload_name:
        refined_workload_name = workload_name.split(":")[0]
    else:
        refined_workload_name = workload_name
    return refined_workload_name

def parse_workload_signature(workload_signature):
    splitted_workload_signature = workload_signature.split("_")

    if "no-migration" not in workload_signature:
        fast_memory_ratio = int(splitted_workload_signature[-1])
        thp = splitted_workload_signature[-2]
        mig_policy = splitted_workload_signature[-3]
        workload_name = "_".join(splitted_workload_signature[:-3])
    else:
        fast_memory_ratio = 0
        thp = splitted_workload_signature[-1]
        mig_policy = splitted_workload_signature[-2]
        workload_name = "_".join(splitted_workload_signature[:-2])
    mig_policy = refine_migration_policy(mig_policy)
    refined_workload_name = refine_workload_name(workload_name)
    abbr_workload_name = abbreviate_workload_name(refined_workload_name)

    return fast_memory_ratio, thp, mig_policy, abbr_workload_name
