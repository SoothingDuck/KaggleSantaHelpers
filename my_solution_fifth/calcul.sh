#!/bin/bash

#my_solution_fourth_num_elves_900_prod_0_5_minutes_60_ratio_random_0_95.csv

for NB_ELVES in 900
do
	for PRODUCTIVITY in 3.0 3.1 3.2 3.4 3.5 3.6 3.7 3.8 3.9 4.0
	do
		for LAST_MINUTE in 120
		do
			for RATIO_RANDOM in 0.8 0.81 0.82 0.83 0.84 0.85 0.86 0.87 0.88 0.89 0.90 0.91 0.92 0.93 0.94 0.95
			do
				PRODUCTIVITY_STR=$(echo $PRODUCTIVITY | sed 's/\./_/')
				RATIO_RANDOM_STR=$(echo $RATIO_RANDOM | sed 's/\./_/')
				FILENAME="../DATA/my_solution_fourth_num_elves_${NB_ELVES}_prod_${PRODUCTIVITY_STR}_minutes_${LAST_MINUTE}_ratio_random_${RATIO_RANDOM_STR}.csv"

				if [ -e $FILENAME ]
				then
					echo "$FILENAME already exists..."
				else
					python MySolution.py $NB_ELVES "$PRODUCTIVITY" $LAST_MINUTE "$RATIO_RANDOM"
				fi
			done
		done
	done
done
