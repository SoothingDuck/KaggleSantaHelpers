#!/bin/bash

for NB_TOYS in 100000
do
	for NB_ELVES in 5 10
	do
		for PRODUCTIVITY in 2.5 3.0 3.5 3.75 4.0
		do
			for LAST_MINUTE in 30 60 120
			do
				PRODUCTIVITY_STR=$(echo $PRODUCTIVITY | sed 's/\./_/')
				FILENAME="../DATA/my_solution_third_num_elves_${NB_ELVES}_num_toys_${NB_TOYS}_prod_${PRODUCTIVITY_STR}_minutes_${LAST_MINUTE}.csv"

				if [ -e $FILENAME ]
				then
					echo "$FILENAME already exists..."
				else
					python MySolution.py $NB_ELVES $NB_TOYS "3.5" $LAST_MINUTE
				fi
			done
		done
	done
done
