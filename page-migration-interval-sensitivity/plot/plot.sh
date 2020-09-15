if [ $# -eq 0 ]
then
	echo "Usage: $0 <result dir>"
	exit
fi

python3 get_elapsed_time.py -result_dir $1 | sort > $1/elapsed_time.txt
python3 get_normalized_performance.py -data $1/elapsed_time.txt | sort > $1/normalized_performance.txt
python3 plot_page_migration_interval_sensitivity.py -data $1/normalized_performance.txt -result_dir $1
