#!/usr/bin/env python
# -*- coding: utf-8 -*-

from toypool import ToyPool
from elfpool import ElfPool

import datetime
import time
import os
import csv

# ======================================================================= #
# === MAIN === #

if __name__ == '__main__':

    start = time.time()

    # Définition de quelques variables
    working_date = datetime.date(2014, 1, 1)

    NUM_ELVES = 900
    NUM_TOYS = 100000
    NUM_TOYS = 20000

    toy_file = os.path.join(os.getcwd(), '..', 'DATA', 'toys_rev2.csv')
    soln_file = os.path.join(os.getcwd(), '..', 'DATA', 'my_solution_num_elves_%d_num_toys_%d.csv' % (NUM_ELVES, NUM_TOYS))

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
        while not myelfpool.empty_for_date(working_date):
            if mytoypool.empty():
                break

            if len(mytoypool) % 1000 == 0:
                print("TOYPOOL LEN : %d" % len(mytoypool))

            elf = myelfpool.next_available_elf()
            elf.apply_strategy_for(mytoypool, myelfpool, wcsv)

        # Go to next working date
        working_date = working_date + datetime.timedelta(days=1)

    print 'total runtime = {0}'.format(time.time() - start)
