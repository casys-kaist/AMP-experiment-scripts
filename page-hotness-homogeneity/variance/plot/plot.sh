if [ $# -eq 0 ]
then
	echo "Usage: $0 <result dir>"
	exit
fi

#python3 get_stdev_li.py -result_dir $1 | sort > $1/stdev_li.txt
python3 plot_cdf.py -data $1/stdev_li.txt -result_dir $1
