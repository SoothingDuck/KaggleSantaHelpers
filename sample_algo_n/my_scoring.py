# -*- coding: utf-8 -*-

import sys
import os
import csv
import time
import math
import datetime

from hours import Hours
from toy import Toy
from elf import Elf


# ======================================================================= #
# === MAIN === #

if __name__ == '__main__':

    def usage():
        print "python SantasHelpers_Evaluation_Metric.py SOLUTION_FILE"

    if len(sys.argv[1:]) != 1:
        usage()
        sys.exit(1)

    start = time.time()

    sub_file = sys.argv[1]

    fcsv = csv.reader(open(sub_file, "rb"))
    fcsv.next()

    last_row = None
    last_toy_timestamp = None
    hash_elves = {}

    i = 0
    for row in fcsv:
        i += 1
        toy_id, elf_id, ts, dur = row
        if not hash_elves.has_key(int(elf_id)):
            hash_elves[int(elf_id)] = 1

        year, month, day, hour, minute = ts.split(" ")
        elf_timestamp = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
        duration = int(dur)

        current_toy_timestamp = elf_timestamp + datetime.timedelta(minutes=duration)
        if last_toy_timestamp is None:
            last_toy_timestamp = current_toy_timestamp
	    last_row = row

        if current_toy_timestamp > last_toy_timestamp:
            last_toy_timestamp = current_toy_timestamp
	    last_row = row

        if i % 1000 == 0:
            print "%d lignes traitées" % i

    nb_elves = len(hash_elves.keys())
    last_minute = int(((last_toy_timestamp - datetime.datetime(2014, 1, 1, 0, 0)).total_seconds())/60)
    score = last_minute * math.log(1.0 + nb_elves)
    
    print last_toy_timestamp
    print last_row
    print last_minute
    print '  Score = {0}'.format(score)
    print 'total time = {0}'.format(time.time() - start)




