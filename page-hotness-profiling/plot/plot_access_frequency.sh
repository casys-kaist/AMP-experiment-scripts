if [ $# -eq 0 ]
then
	echo "Usage: $0 <result dir>"
	exit
fi

python3 get_uniq_lines.py -result_dir $1
python3 get_access_frequency_data.py -result_dir $1
python3 plot_access_frequency.py -result_dir $1
