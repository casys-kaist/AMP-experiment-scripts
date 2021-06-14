if [ $# -eq 0 ]
then
	echo "Usage: $0 <result dir>"
	exit
fi

python3 plot_fast_memory_ratio_sensitivity.py -data $1/normalized_performance_geomean.txt -result_dir $1
