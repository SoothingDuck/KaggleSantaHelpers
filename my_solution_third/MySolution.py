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
    PRODUCTIVITY_THRESHOLD = 3.75
    MINUTES_LEFT_END_OF_DAY = 60

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

        # Etape 1 : Prendre le prochain elfe disponible
        elf = myelfpool.next_available_elf()

        # Etape 2 : Recupérer la productivité de l'elfe
        productivity = elf.get_productivity()
        
        # Etape 2, Cas 1 : La productivité est supérieure au seuil
        if productivity > PRODUCTIVITY_THRESHOLD:
            # Etape 3 : Récupérer le jouet le plus gros disponible
            toy = mytoypool.get_biggest_toy()

            # Etape 4 : Faire le jouet
            elf.make_toy(toy, wcsv)

            # Etape 5 : Mettre à jour l'elfe dans le pool d'elfes
            myelfpool.update_elf(elf)

        # Etape 2, Cas 2 : La productivité est inférieure au seuil
        else:

            # Etape 2.2 : Calculer le nombre de minutes restantes avant la fin de la journée
            minutes_left = elf.num_of_working_minutes_left()

            # Etape 3.2 : Avec la productivité, calculer le nombre de minutes max pouvant être consacrées à un jouet
            productivity = elf.get_productivity()
            toy_max_minutes = int(minutes_left*productivity)

            # Etape 4.2 : Selectionner un jouet disposant d'un nombre de minutes inférieur à toy_max_minutes
            toy_expected_duration = random.randint(1, toy_max_minutes)
            toy = mytoypool.get_toy_by_duration(toy_expected_duration)

            # Etape 4.2, Cas 1 : Un jouet de ce type n'existe pas
            if toy is None:
                # On est à la fin de la journée ?
                if minutes_left < MINUTES_LEFT_END_OF_DAY:
                    # Mieux vaut attendre demain
                    elf.wait_till_next_day()
                    # Mise à jour de l'elfe dans le pool
                    myelfpool.update_elf(elf)
                else:
                    # Sinon pas trop le choix on réalise la prochain jouet le plus "court"
                    toy = mytoypool.get_next_shortest_toy()
                    elf.make_toy(toy, wcsv)

                    myelfpool.update_elf(elf)
                    
            else:
            # Etape 4.2, Cas 2 : Un tel jouet existe, c'est super on le réalise
                elf.make_toy(toy, wcsv)

                myelfpool.update_elf(elf)



    print 'total runtime = {0}'.format(time.time() - start)
