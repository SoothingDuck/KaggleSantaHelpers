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
    myelfpool = ElfPool()
    myelfpool.init_with(NUM_ELVES)

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
            print("TOYPOOL LEN : %d, ELFPOOL LEN : %d" % (mytoypool.length_available_list(), len(myelfpool)))

        # Etape 1 : Mise à jour de l'available list en rapport avec le elfpool actuel
        mytoypool.fill_available_list_according_to(myelfpool)

        # Etape 2 : Recuperer un jouet de l'available list
        toy = mytoypool.pop_toy_of_available_list()

        # Etape 3 : Evaluer quel sera l'elfe qui pourra réaliser celui ci le plus tôt
        tmp = []
        while len(myelfpool) > 0:
            elf = myelfpool.next_available_elf()
            elf_future_toy_timestamp = elf.evaluate_finish_time_for(toy)
            tmp.append((elf_future_toy_timestamp, elf))
        heapq.heapify(tmp)
        elf_future_toy_timestamp, elf = heapq.heappop(tmp)

        # Etape 4 : L'elfe qui finira le plus tôt fait le jouet
        elf.make_toy(toy, wcsv)

        # Etape 5 : Reforme le pool d'elfe
        # 1. l'elfe qui a bossé
        myelfpool.add_elf(elf)

        # 2. Les autres
        for elf_timestamp, elf in tmp:
            myelfpool.add_elf(elf)

        #while len(tmp) > 0:
        #    elf_future_toy_timestamp, elf = heapq.heappop(tmp)
        #    myelfpool.add_elf(elf)
            
        # On continue



    print 'total runtime = {0}'.format(time.time() - start)
