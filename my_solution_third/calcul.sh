#!/bin/bash

for NB_TOYS in 10000000
do
	for NB_ELVES in 500 700 900
	do
			for LAST_MINUTE in 120
			do
				FILENAME="../DATA/my_solution_third_num_elves_${NB_ELVES}_num_toys_${NB_TOYS}_prod_3_5_minutes_${LAST_MINUTE}.csv"

				if [ -e $FILENAME ]
				then
					echo "$FILENAME already exists..."
				else
					python MySolution.py $NB_ELVES $NB_TOYS "3.5" $LAST_MINUTE
				fi
			done
	done
done
