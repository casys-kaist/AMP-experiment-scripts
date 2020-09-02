if [ $# -eq 0 ]
then
	echo "Usage: $0 <result dir>"
	exit
fi

python3 get_performance.py -result_dir $1 > $1/normalized_performance.txt
python3 plot_performance.py -data $1/normalized_performance.txt -result_dir $1
