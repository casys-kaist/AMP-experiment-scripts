#!/usr/bin/env python3

"""
   docker_process_pauser.py

    Created on: Dec. 18, 2018
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import psutil

def get_container_pid_li(container_id):
    pid_li = []
    task_file_path = "/sys/fs/cgroup/memory/docker/%s/tasks" % (container_id)
    task_file = open(task_file_path)
    for line in task_file:
        pid_li.append(int(line.strip()))
    return pid_li

def suspend_all_processes(container_id_li):
    for container_id in container_id_li:
        pid_li = get_container_pid_li(container_id)
        for pid in pid_li:
            try:
                psutil.Process(pid).suspend()
            except psutil.NoSuchProcess as e:
                pass

def resume_all_processes(container_id_li):
    for container_id in container_id_li:
        pid_li = get_container_pid_li(container_id)
        for pid in pid_li:
            try:
                psutil.Process(pid).resume()
            except psutil.NoSuchProcess as e:
                pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-command", type=str, default="pause")
    parser.add_argument("-container_id", type=str, action="append", required=True)
    args = parser.parse_args()

    if args.command == "pause":
        suspend_all_processes(args.container_id)
    elif args.command == "unpause":
        resume_all_processes(args.container_id)

if __name__ == '__main__':
    main()
