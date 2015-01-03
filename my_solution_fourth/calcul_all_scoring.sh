#!/bin/bash

SCORE_FILENAME="../scores.csv"

echo "filename,nb_elves,nb_toys,last_toy_timestamp,score" > $SCORE_FILENAME

for FILENAME in $(ls -rt ../DATA/*.csv | grep solution)
do
	echo "Traitement $FILENAME"
	python my_scoring.py $FILENAME >> $SCORE_FILENAME

done
