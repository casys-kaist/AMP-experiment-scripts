* Please install [linux-v4.15-page-hotness-profiling](https://github.com/casys-kaist/linux-v4.15-page-hotness-profiling) in the guest VM.
* This Linux kernel has been used for visualize memory accesses.

* Run experiments
```
python3 experiment.py -result_dir ~/experiment-results
```
* Plot graphs
```
cd plot
./plot_access_frequency.sh <result dir>
```
