if [ $# -eq 0 ]
then
	echo "Usage: $0 <result dir>"
	exit
fi

python3 get_huge_page_ratio.py -result_dir $1 > $1/huge_page_ratio.txt
