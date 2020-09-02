if [ $# -eq 0 ]
then
	echo "Usage: $0 <result dir>"
	exit
fi

# plot performance
python3 get_normalized_performance.py -result_dir $1 > $1/normalized_performance.txt
python3 plot_migration_policy_performance_motivation.py -data $1/normalized_performance.txt -result_dir $1
python3 plot_migration_policy_performance_potential.py -data $1/normalized_performance.txt -result_dir $1
python3 plot_migration_policy_performance_ideal.py -data $1/normalized_performance.txt -result_dir $1
python3 plot_migration_policy_performance_evaluation.py -data $1/normalized_performance.txt -result_dir $1

# plot average feature values
python3 get_page_migration_stability_avg.py -result_dir $1 | sort > $1/page_migration_stability_avg.txt
python3 get_accessed_pages_ratio_avg.py -result_dir $1 | sort > $1/accessed_pages_ratio_avg.txt
python3 get_fast_memory_hit_ratio_avg.py -result_dir $1 | sort > $1/fast_memory_hit_ratio_avg.txt

# plot feature value changes
python3 get_page_migration_stability.py -result_dir $1 > $1/page_migration_stability.txt
python3 get_accessed_pages_ratio.py -result_dir $1 > $1/accessed_pages_ratio.txt
python3 get_fast_memory_hit_ratio.py -result_dir $1 > $1/fast_memory_hit_ratio.txt
python3 get_fast_memory_hit_ratio_moving_avg.py -result_dir $1 > $1/fast_memory_hit_ratio_moving_avg.txt
python3 plot_feature_value_changes.py -data $1/page_migration_stability.txt -result_dir $1
python3 plot_feature_value_changes.py -data $1/accessed_pages_ratio.txt -result_dir $1
python3 plot_feature_value_changes.py -data $1/fast_memory_hit_ratio.txt -result_dir $1
python3 plot_feature_value_changes.py -data $1/fast_memory_hit_ratio_moving_avg.txt -result_dir $1
python3 plot_feature_value_avg.py -data $1/accessed_pages_ratio_avg.txt -result_dir $1

python3 plot_fast_memory_hit_ratio_moving_avg_subplot.py -data $1/fast_memory_hit_ratio_moving_avg.txt -result_dir $1

# plot feature value scatter charts
python3 get_feature_gap_performance.py -result_dir $1 > $1/feature.txt
cat $1/feature.txt | sort | grep "Page Migration Stability" > $1/page_migration_stability.txt
cat $1/feature.txt | sort | grep "Accessed Page Ratio" > $1/accessed_pages_ratio.txt
cat $1/feature.txt | sort | grep "Fast Memory Hit Ratio" > $1/fast_memory_hit_ratio.txt
python3 plot_feature_gap_performance_scatter_chart.py -data $1/page_migration_stability.txt -result_dir $1
python3 plot_feature_gap_performance_scatter_chart.py -data $1/accessed_pages_ratio.txt -result_dir $1
python3 plot_feature_gap_performance_scatter_chart.py -data $1/fast_memory_hit_ratio.txt -result_dir $1

# plot migration policy selections - timeline
python3 get_migration_policy_selections.py -result_dir $1 > $1/migration_policy_selections.txt
python3 plot_migration_policy_selections_timeline.py -data $1/migration_policy_selections.txt -result_dir $1
python3 plot_migration_policy_selections_timeline_subplot.py -data $1/migration_policy_selections.txt -result_dir $1

# plot migration policy selections - stacked bar
python3 get_migration_policy_selections_ratio.py -result_dir $1 | sort > $1/migration_policy_selections_ratio.txt
python3 plot_migration_policy_selections_ratio_stacked_bar.py -data $1/migration_policy_selections_ratio.txt -result_dir $1
