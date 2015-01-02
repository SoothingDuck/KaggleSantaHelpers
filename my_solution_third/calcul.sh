#!/bin/bash

for NB_TOYS in 200000
do
	for NB_ELVES in 500 700 900
	do
		for PRODUCTIVITY in 2.5 3.0 3.5
		do
			for LAST_MINUTE in 15 30 60
			do
				python MySolution.py $NB_ELVES $NB_TOYS $PRODUCTIVITY $LAST_MINUTE
			done
		done
	done
done
