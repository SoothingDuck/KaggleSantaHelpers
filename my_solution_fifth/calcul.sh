#!/bin/bash

#my_solution_fifth_num_elves_900_prod_4_0_minutes_120_ratio_random_0_89_min_duration_1000.csv

for NB_ELVES in 900
do
	for PRODUCTIVITY in 0.25 0.5 1 2 2.5 3 3.5 4
	do
		for LAST_MINUTE in 30 60 120
		do
			for RATIO_RANDOM in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
			do
				for MIN_DURATION in 10 100 500 1000 2000 5000 10000 20000
				do
					PRODUCTIVITY_STR=$(echo $PRODUCTIVITY | sed 's/\./_/')
					RATIO_RANDOM_STR=$(echo $RATIO_RANDOM | sed 's/\./_/')
					FILENAME="../DATA/my_solution_fifth_num_elves_${NB_ELVES}_prod_${PRODUCTIVITY_STR}_minutes_${LAST_MINUTE}_ratio_random_${RATIO_RANDOM_STR}_min_duration_${MIN_DURATION}.csv"

					if [ -e $FILENAME ]
					then
						echo "$FILENAME already exists..."
					else
						python MySolution.py $NB_ELVES "$PRODUCTIVITY" $LAST_MINUTE "$RATIO_RANDOM" $MIN_DURATION
					fi
				done
			done
		done
	done
done
