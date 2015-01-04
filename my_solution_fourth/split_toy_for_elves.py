
# -*- coding: utf-8 -*-

import csv
import os, sys
import heapq
from toy import Toy
from elf import Elf

# Num elves
def usage():
    print "Usage : python split_toy_for_elves.py NUM_ELVES"

if len(sys.argv[1:]) != 1:
    usage()
    sys.exit(1)

NUM_ELVES = int(sys.argv[1])

# Toy Heap
toy_heap = []

# Elf Heap
elf_heap = []
for i in xrange(NUM_ELVES):
    heapq.heappush(elf_heap, (0, Elf(i+1)))

# Lecture du fichier des jouets
i = 0
all_toys_filename = os.path.join("..", "DATA", "toys_rev2.csv")
f = open(all_toys_filename, "rb")
fcsv = csv.reader(f)
fcsv.next()
for row in fcsv:
    i += 1
    new_toy = Toy(row[0], row[1], row[2])
    t = new_toy.get_arrival_minute()
    if t % 1440 <= (9*60):
        t = ((t/1440)*1440)+(9*60)
    elif t % 1440 >= (19*60):
        t = (((t/1440)+1)*1440)+(9*60)
    toy_arrival_minute = t
    toy_arrival_day = toy_arrival_minute / 1440
    toy_duration = new_toy.get_duration()

    heapq.heappush(toy_heap, (-(toy_duration), new_toy))

    if i % 1000 == 0:
        print i

    #if i == 1000000:
    #    break

f.close()

# Definition des fichiers
hash_file = {}
for i in xrange(NUM_ELVES):
    filename = os.path.join("..", "DATA", "toy_for_elf_number_%d_out_of_%d.csv" % (i+1, NUM_ELVES))
    hash_file[i+1] = open(filename, "w")
    hash_file[i+1].write("ToyId,Arrival_minute,Duration\n")

# Repartition des jouets
while True:

    if len(toy_heap) <= 0:
        break

    # Prochain elf
    elf_total_duration, elf = heapq.heappop(elf_heap)

    # Prochain jouet
    toy_trash, toy = heapq.heappop(toy_heap)

    # Ecriture fichier
    hash_file[elf.get_id()].write("%d,%d,%d\n" % (int(toy.get_id()), int(toy.get_arrival_minute()), int(toy.get_duration())))

    # Mise à jour elfe
    elf_total_duration += toy.get_duration()
    heapq.heappush(elf_heap, (elf_total_duration, elf))

    # Affichage si besoin
    if len(toy_heap) % 1000 == 0:
        print "Taille Toy Heap => %d" % (len(toy_heap))

