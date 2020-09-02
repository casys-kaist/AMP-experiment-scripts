#!/usr/bin/env python3

"""
   amp.py

    Created on: Jan. 3, 2020
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import numpy as np
from statistics import mean
from lib.amp import *
from lib.stats import *

def moving_average(a, n) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

class AMP:
    def __init__(self,
            result_dir, workload, signature,
            fast_memory_ratio, warm_up, window_size, random_threshold):
        # configurations
        self.result_dir = result_dir
        self.workload = workload
        self.signature = signature
        self.fast_memory_ratio = fast_memory_ratio
        self.warm_up = warm_up
        self.window_size = window_size
        self.random_threshold = random_threshold

        # variables
        self.epoch_cnt = 0
        self.fast_memory_hit_ratio_hist = { MIG_POLICY_LRU: [], MIG_POLICY_LFU: [] }

    def get_stats(self):
        num_total_pages = 0
        num_page_migrations = 0
        num_accessed_pages = 0
        num_fast_memory_hit_pages = 0
        lru_num_fast_memory_hit_pages = 0
        lfu_num_fast_memory_hit_pages = 0
        lru_fast_memory_hit_ratio = 0
        lfu_fast_memory_hit_ratio = 0
        for cgroup in self.workload.get_cgroup_li():
            num_total_pages += cgroup.get_int("memory.migration.stats.num_total_pages")
            num_page_migrations += cgroup.get_int("memory.migration.stats.num_page_migrations")
            num_accessed_pages += cgroup.get_int("memory.migration.stats.num_accessed_pages")
            num_fast_memory_hit_pages += cgroup.get_int("memory.migration.stats.num_fast_memory_hit_pages")
            lru_num_fast_memory_hit_pages += cgroup.get_int("memory.migration.stats.lru.num_fast_memory_hit_pages")
            lfu_num_fast_memory_hit_pages += cgroup.get_int("memory.migration.stats.lfu.num_fast_memory_hit_pages")

        if num_total_pages != 0:
            page_migration_stability = (num_total_pages - num_page_migrations) / num_total_pages
            accessed_pages_ratio = num_accessed_pages / num_total_pages
            fast_memory_hit_ratio = num_fast_memory_hit_pages / num_total_pages
            if num_accessed_pages != 0:
                fast_memory_access_ratio = num_fast_memory_hit_pages / num_accessed_pages
            else:
                fast_memory_access_ratio = 0

            if self.prev_chosen_mig_policy in self.fast_memory_hit_ratio_hist.keys():
                lru_fast_memory_hit_ratio = lru_num_fast_memory_hit_pages / num_total_pages
                lfu_fast_memory_hit_ratio = lfu_num_fast_memory_hit_pages / num_total_pages
                print("lru", lru_fast_memory_hit_ratio, "lfu", lfu_fast_memory_hit_ratio)

                self.fast_memory_hit_ratio_hist[MIG_POLICY_LRU].append(lru_fast_memory_hit_ratio)
                self.fast_memory_hit_ratio_hist[MIG_POLICY_LFU].append(lfu_fast_memory_hit_ratio)
                for mig_policy in self.fast_memory_hit_ratio_hist.keys():
                    if len(self.fast_memory_hit_ratio_hist[mig_policy]) > self.window_size:
                        self.fast_memory_hit_ratio_hist[mig_policy] = self.fast_memory_hit_ratio_hist[mig_policy][1:]
        else:
            page_migration_stability = 0
            accessed_pages_ratio = 0
            fast_memory_hit_ratio = 0
            fast_memory_access_ratio = 0
        fast_memory_hit_ratio_moving_avg = 0
        return page_migration_stability, accessed_pages_ratio,\
                fast_memory_hit_ratio, lru_fast_memory_hit_ratio, lfu_fast_memory_hit_ratio,\
                fast_memory_access_ratio

    def __choose_mig_policy(self):
        if len(self.fast_memory_hit_ratio_hist[MIG_POLICY_LRU]) > 0:
            lru_fast_memory_hit_ratio_mean = mean(self.fast_memory_hit_ratio_hist[MIG_POLICY_LRU])
        else:
            lru_fast_memory_hit_ratio_mean = 0
        if len(self.fast_memory_hit_ratio_hist[MIG_POLICY_LFU]) > 0:
            lfu_fast_memory_hit_ratio_mean = mean(self.fast_memory_hit_ratio_hist[MIG_POLICY_LFU])
        else:
            lfu_fast_memory_hit_ratio_mean = 0
        print("epoch", self.epoch_cnt, "lru_fmhr_mean", lru_fast_memory_hit_ratio_mean, "lfu_fmhr_mean", lfu_fast_memory_hit_ratio_mean)
        if lru_fast_memory_hit_ratio_mean >= lfu_fast_memory_hit_ratio_mean:
            return MIG_POLICY_LRU
        if lru_fast_memory_hit_ratio_mean < lfu_fast_memory_hit_ratio_mean:
            return MIG_POLICY_LFU

    def choose_mig_policy(self):
        self.epoch_cnt += 1

        if self.epoch_cnt > 1:
            page_migration_stability, accessed_pages_ratio,\
                    fast_memory_hit_ratio, lru_fast_memory_hit_ratio, lfu_fast_memory_hit_ratio,\
                    fast_memory_access_ratio\
                    = self.get_stats()

            record_stats_single(self.result_dir, self.signature, "page_migration_stability",
                    "%f\n" % (page_migration_stability))
            record_stats_single(self.result_dir, self.signature, "accessed_pages_ratio",
                    "%f\n" % (accessed_pages_ratio))
            record_stats_single(self.result_dir, self.signature, "fast_memory_hit_ratio",
                    "%f\n" % (fast_memory_hit_ratio))
            record_stats_single(self.result_dir, self.signature, "lru_fast_memory_hit_ratio",
                    "%f\n" % (lru_fast_memory_hit_ratio))
            record_stats_single(self.result_dir, self.signature, "lfu_fast_memory_hit_ratio",
                    "%f\n" % (lfu_fast_memory_hit_ratio))
            record_stats_single(self.result_dir, self.signature, "fast_memory_access_ratio",
                    "%f\n" % (fast_memory_access_ratio))

        if self.epoch_cnt <= self.warm_up:
            chosen_mig_policy = MIG_POLICY_PSEUDO_RANDOM
        else:
            random_threshold = (self.fast_memory_ratio + self.random_threshold)
            if accessed_pages_ratio >= random_threshold:
                print("Choose pseudo random")
                chosen_mig_policy = MIG_POLICY_PSEUDO_RANDOM
            else:
                print("Adaptive selection")
                chosen_mig_policy = self.__choose_mig_policy()

        print("[CHOSEN] %d" % (chosen_mig_policy))

        record_stats_single(self.result_dir, self.signature, "mig_policy",
                "%d\n" % (chosen_mig_policy))
        self.prev_chosen_mig_policy = chosen_mig_policy
        return chosen_mig_policy
