#!/bin/bash

#my_solution_fourth_num_elves_900_prod_0_5_minutes_60.csv

for NB_ELVES in 900
do
	for PRODUCTIVITY in 0.0 0.25 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0
	do
		for LAST_MINUTE in 60
		do
			for RATIO in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
			do
				PRODUCTIVITY_STR=$(echo $PRODUCTIVITY | sed 's/\./_/')
				RATIO_STR=$(echo $RATIO | sed 's/\./_/')
				FILENAME="../DATA/my_solution_fourth_num_elves_${NB_ELVES}_prod_${PRODUCTIVITY_STR}_minutes_${LAST_MINUTE}_ratio_${RATIO_STR}.csv"

				if [ -e $FILENAME ]
				then
					echo "$FILENAME already exists..."
				else
					python MySolution.py $NB_ELVES "$PRODUCTIVITY" $LAST_MINUTE "$RATIO"
				fi
			done
		done
	done
done
