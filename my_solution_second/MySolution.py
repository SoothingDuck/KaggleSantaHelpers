#!/usr/bin/env python
# -*- coding: utf-8 -*-

from toypool import ToyPool
from elfpool import ElfPool

import datetime
import time
import os
import csv
import sys
import heapq
# ======================================================================= #
# === MAIN === #

if __name__ == '__main__':

    def usage():
        print "python MySolution.py NUM_ELVES NUM_TOYS"

    if len(sys.argv[1:]) != 2:
        usage()
        sys.exit(1)

    start = time.time()

    # Définition de quelques variables
    working_date = datetime.date(2014, 1, 1)

    NUM_ELVES = int(sys.argv[1])
    NUM_TOYS = int(sys.argv[2])

    toy_file = os.path.join(os.getcwd(), '..', 'DATA', 'toys_rev2.csv')
    soln_file = os.path.join(os.getcwd(), '..', 'DATA', 'my_solution_second_num_elves_%d_num_toys_%d.csv' % (NUM_ELVES, NUM_TOYS))

    # Création du pool d'elfes
    myelfpool = ElfPool(NUM_ELVES)

    # Création du pool de jouets
    mytoypool = ToyPool()
    mytoypool.add_file_content(toy_file, NUM_TOYS)

    # Fichier dans lequel logger la solution
    w = open(soln_file, 'wb')
    wcsv = csv.writer(w)
    wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])

    # Début de l'algorithme
    while not mytoypool.empty():

        # Apply strategy for all elves in pool 
        #  Pour chaque elfe:
        #   1 jouet au hasard parmi ceux disponibles
        #   Si on peut traiter l'objet dans la journée, le faire et mettre à jour la date de disponibilité de l'elfe
        #   Sinon planifier l'objet pour le lendemain matin et le traiter et remplir le reste de la journée avec des objets "courts"
        if mytoypool.length_available_list() % 1000 == 0:
            print("TOYPOOL LEN : %d, ELFPOOL LEN : %d" % (mytoypool.length_available_list()+mytoypool.length_waiting_list(), len(myelfpool)))

        # Etape 1 : Mise à jour de l'available list en rapport avec le elfpool actuel
        # mytoypool.fill_available_list_according_to(myelfpool)

        # Etape 2 : Recuperer un jouet de la waiting list
        toy = mytoypool.pop_toy_of_waiting_list()
        toy_timestamp = toy.get_min_possible_working_start_time()

        # Etape 3 : Evaluer quel sera l'elfe qui pourra réaliser celui ci le plus tôt
        tmp = []
        min_future_timestamp = None
        elf_kept = None
        for elf in myelfpool.elf_list():
            if toy_timestamp <= elf.get_next_available_working_time():
                elf_future_toy_timestamp = elf.evaluate_finish_time_for(toy)
                if min_future_timestamp is None:
                    min_future_timestamp = elf_future_toy_timestamp
                    elf_kept = elf

                if elf_future_toy_timestamp < min_future_timestamp:
                    min_future_timestamp = elf_future_toy_timestamp
                    elf_kept = elf

        # Etape 4 : L'elfe qui finira le plus tôt fait le jouet
        elf_kept.make_toy(toy, wcsv)

        # Etape 5 : Reforme le pool d'elfe
        myelfpool.update_elf(elf_kept)

        #while len(tmp) > 0:
        #    elf_future_toy_timestamp, elf = heapq.heappop(tmp)
        #    myelfpool.add_elf(elf)
            
        # On continue



    print 'total runtime = {0}'.format(time.time() - start)
