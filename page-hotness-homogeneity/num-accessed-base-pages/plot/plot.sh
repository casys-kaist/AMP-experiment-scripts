if [ $# -eq 0 ]
then
	echo "Usage: $0 <result dir>"
	exit
fi

python3 get_accessed_base_page_ratio.py -result_dir $1 > $1/accessed_base_page_ratio.txt
