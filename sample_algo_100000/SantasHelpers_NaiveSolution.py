""" Simple solution to the Santa 2014 Kaggle competition evaluation metric. 
This solution takes each toy in turn (in chronological order) and assigns the next
available elf to it. """
__author__ = 'Joyce Noah-Vanhoucke'
__date__ = 'November 24, 2014'

import sys
import os
import csv
import math
import heapq
import time
import datetime

from hours import Hours
from toy import Toy
from elf import Elf

# ========================================================================== #

def read_toys(toy_file, num_toys):
    """ Reads the toy file and returns a dictionary of Toys.
    Toy file format: ToyId, Arrival_time, Duration
        ToyId: toy id
        Arrival_time: time toy arrives. Format is: YYYY MM DD HH MM (space-separated)
        Duration: duration in minutes to build toy
    :param toy_file: toys input file
    :param hrs: hours object
    :param num_toys: total number of toys to build
    :return: Dictionary of toys
    """
    i = 0
    toy_heap = []
    with open(toy_file, 'rb') as f:
        fcsv = csv.reader(f)
        fcsv.next()  # header row
        for row in fcsv:
	    i += 1
            new_toy = Toy(row[0], row[1], row[2])
            heapq.heappush(toy_heap, (int(row[2]), new_toy))
	    if len(toy_heap) % 1000 == 0:
	    	print len(toy_heap)

            if i >= num_toys:
	    	break

    if len(toy_heap) != num_toys:
        print '\n ** Read a file with {0} toys, expected {1} toys. Exiting.'.format(len(toy_heap), num_toys)
        exit(-1)
    return toy_heap

def create_elves(NUM_ELVES):
    """ Elves are stored in a sorted list using heapq to maintain their order by next available time.
    List elements are a tuple of (next_available_time, elf object)
    :return: list of elves
    """
    list_elves = []
    for i in xrange(1, NUM_ELVES+1):
        elf = Elf(i)
        heapq.heappush(list_elves, (elf.next_available_time, elf))
    return list_elves


def assign_elf_to_toy(input_time, current_elf, current_toy, hrs):
    """ Given a toy, assigns the next elf to the toy. Computes the elf's updated rating,
    applies the rest period (if any), and sets the next available time.
    :param input_time: list of tuples (next_available_time, elf)
    :param current_elf: elf object
    :param current_toy: toy object
    :param hrs: hours object
    :return: list of elves in order of next available
    """
    start_time = hrs.next_sanctioned_minute(input_time)  # double checks that work starts during sanctioned work hours
    duration = int(math.ceil(current_toy.duration / current_elf.rating))
    sanctioned, unsanctioned = hrs.get_sanctioned_breakdown(start_time, duration)

    if unsanctioned == 0:
        return hrs.next_sanctioned_minute(start_time + duration), duration
    else:
        return hrs.apply_resting_period(start_time + duration, unsanctioned), duration


def solution_firstAvailableElf(toy_file, soln_file, myelves):
    """ Creates a simple solution where the next available elf is assigned a toy. Elves do not start
    work outside of sanctioned hours.
    :param toy_file: filename for toys file (input)
    :param soln_file: filename for solution file (output)
    :param myelves: list of elves in a priority queue ordered by next available time
    :return:
    """
    i = 0
    hrs = Hours()
    ref_time = datetime.datetime(2014, 1, 1, 0, 0)
    row_count = 0

    with open(toy_file, 'rb') as f:
        toysfile = csv.reader(f)
        toysfile.next()  # header row

        with open(soln_file, 'wb') as w:
            wcsv = csv.writer(w)
            wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])

            for row in toysfile:
	    	i += 1
                current_toy = Toy(row[0], row[1], row[2])

                # get next available elf
                elf_available_time, current_elf = heapq.heappop(myelves)

                work_start_time = elf_available_time
                if current_toy.arrival_minute > elf_available_time:
                    work_start_time = current_toy.arrival_minute

                # work_start_time cannot be before toy's arrival
                if work_start_time < current_toy.arrival_minute:
                    print 'Work_start_time before arrival minute: {0}, {1}'.\
                        format(work_start_time, current_toy.arrival_minute)
                    exit(-1)

                current_elf.next_available_time, work_duration = \
                    assign_elf_to_toy(work_start_time, current_elf, current_toy, hrs)
                current_elf.update_elf(hrs, current_toy, work_start_time, work_duration)

                # put elf back in heap
                heapq.heappush(myelves, (current_elf.next_available_time, current_elf))

                # write to file in correct format
                tt = ref_time + datetime.timedelta(seconds=60*work_start_time)
                time_string = " ".join([str(tt.year), str(tt.month), str(tt.day), str(tt.hour), str(tt.minute)])
                wcsv.writerow([current_toy.id, current_elf.id, time_string, work_duration])

		if i >= NUM_TOYS:
			break


def solution_smallBigQueueElf(toy_file, soln_file, myelves):
    """ Creates a simple solution where the next available elf is assigned a toy. Elves do not start
    work outside of sanctioned hours.
    :param toy_file: filename for toys file (input)
    :param soln_file: filename for solution file (output)
    :param myelves: list of elves in a priority queue ordered by next available time
    :return:
    """
    i = 0
    hrs = Hours()
    ref_time = datetime.datetime(2014, 1, 1, 0, 0)
    row_count = 0

    all_toys = read_toys(toy_file, NUM_TOYS)

    big_duration_threshold = 60
    big_productivity_threshold = 3.0

    big_toys = []
    small_toys = []

    big_productivity_elves = []
    low_productivity_elves = []

    for elf_available_time, elf in myelves:
        if elf.rating < big_productivity_threshold:
		heapq.heappush(low_productivity_elves, (elf_available_time, elf))
	else:
		heapq.heappush(big_productivity_elves, (elf_available_time, elf))

    for elf_available_time, elf in low_productivity_elves:
	    print elf

    sys.exit(1)

    i = 0
    # Round
    while len(all_toys) > 0:
	toy = heapq.heappop(all_toys)
	i += 1
	if i % 1000 == 0:
		print "Nb jouet traite : %d" % i

    sys.exit(0)

    with open(toy_file, 'rb') as f:
        toysfile = csv.reader(f)
        toysfile.next()  # header row

        with open(soln_file, 'wb') as w:
            wcsv = csv.writer(w)
            wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])

            for row in toysfile:
	    	i += 1
                current_toy = Toy(row[0], row[1], row[2])
		
		# Tri par jouet long-court
		duration = int(row[2])
		if duration > 60:
                    heapq.heappush(big_toys, (duration, current_toy))
                else:
                    heapq.heappush(small_toys, (duration, current_toy))

                # get next available elf
                elf_available_time, current_elf = heapq.heappop(myelves)

                work_start_time = elf_available_time
                if current_toy.arrival_minute > elf_available_time:
                    work_start_time = current_toy.arrival_minute

                # work_start_time cannot be before toy's arrival
                if work_start_time < current_toy.arrival_minute:
                    print 'Work_start_time before arrival minute: {0}, {1}'.\
                        format(work_start_time, current_toy.arrival_minute)
                    exit(-1)

                current_elf.next_available_time, work_duration = \
                    assign_elf_to_toy(work_start_time, current_elf, current_toy, hrs)
                current_elf.update_elf(hrs, current_toy, work_start_time, work_duration)

                # put elf back in heap
                heapq.heappush(myelves, (current_elf.next_available_time, current_elf))

                # write to file in correct format
                tt = ref_time + datetime.timedelta(seconds=60*work_start_time)
                time_string = " ".join([str(tt.year), str(tt.month), str(tt.day), str(tt.hour), str(tt.minute)])
                wcsv.writerow([current_toy.id, current_elf.id, time_string, work_duration])

		if i >= NUM_TOYS:
			break

# ======================================================================= #
# === MAIN === #

if __name__ == '__main__':

    start = time.time()

    NUM_ELVES = 900
    NUM_TOYS = 100000

    toy_file = os.path.join(os.getcwd(), '..', 'DATA', 'toys_rev2.csv')
    soln_file = os.path.join(os.getcwd(), '..', 'DATA', 'sampleSubmission_rev2_naive_%d.csv' % NUM_TOYS)

    myelves = create_elves(NUM_ELVES)
    #solution_firstAvailableElf(toy_file, soln_file, myelves)
    solution_smallBigQueueElf(toy_file, soln_file, myelves)

    print 'total runtime = {0}'.format(time.time() - start)
