if [ $# -eq 0 ]
then
	echo "Usage: $0 <result dir>"
	exit
fi

python3 get_migration_policy_selections.py -result_dir $1 > $1/mig_policy_selections.txt
python3 plot_migration_policy_selections_timeline.py -data $1/mig_policy_selections.txt -result_dir $1
