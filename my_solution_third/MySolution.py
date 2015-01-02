#!/usr/bin/env python
# -*- coding: utf-8 -*-

from toypool import ToyPool
from elfpool import ElfPool
from hours import Hours

import math
import datetime
import time
import os
import csv
import sys
import heapq
import random

# ======================================================================= #
# === MAIN === #

if __name__ == '__main__':

    def usage():
        print "python MySolution.py NUM_ELVES NUM_TOYS MAX_PRODUCTIVITY MINUTES_END_OF_DAY"

    if len(sys.argv[1:]) != 4:
        usage()
        sys.exit(1)

    start = time.time()

    # Définition de quelques variables
    working_date = datetime.date(2014, 1, 1)

    NUM_ELVES = int(sys.argv[1])
    NUM_TOYS = int(sys.argv[2])
    PRODUCTIVITY_THRESHOLD = float(sys.argv[3])
    MINUTES_LEFT_END_OF_DAY = int(sys.argv[4])

    PRODUCTIVITY_THRESHOLD_STR = str(PRODUCTIVITY_THRESHOLD).replace(".", "_")

    toy_file = os.path.join(os.getcwd(), '..', 'DATA', 'toys_rev2.csv')
    soln_file = os.path.join(os.getcwd(), '..', 'DATA', 'my_solution_third_num_elves_%d_num_toys_%d_prod_%s_minutes_%d.csv' % (NUM_ELVES, NUM_TOYS, PRODUCTIVITY_THRESHOLD_STR, MINUTES_LEFT_END_OF_DAY))

    # Objet hours
    hrs = Hours()

    # Création du pool d'elfes
    myelfpool = ElfPool(NUM_ELVES)

    # Création du pool de jouets
    mytoypool = ToyPool()
    mytoypool.add_file_content(toy_file, NUM_TOYS)

    # Fichier dans lequel logger la solution
    w = open(soln_file, 'wb')
    wcsv = csv.writer(w)
    wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration', 'Original_Toy_Duration', 'Old_Productivity', 'New_Productivity', 'Sanctioned', 'Unsanctioned'])

    c = 0

    # Début de l'algorithme
    while not mytoypool.empty():

        c += 1

        # Apply strategy for all elves in pool 
        #  Pour chaque elfe:
        #   1 jouet au hasard parmi ceux disponibles
        #   Si on peut traiter l'objet dans la journée, le faire et mettre à jour la date de disponibilité de l'elfe
        #   Sinon planifier l'objet pour le lendemain matin et le traiter et remplir le reste de la journée avec des objets "courts"
        if c % 10000 == 0:
            print("TOYPOOL WAITING LEN : %d, TOYPOOL AVAILABLE LEN : %d, ELFPOOL LEN : %d" % (mytoypool.length_waiting_list(), mytoypool.length_available_list(), len(myelfpool)))

        # Etape 1 : Prendre le prochain elfe disponible
        elf = myelfpool.next_available_elf()

        # Etape 1 Bis : Mettre à jour le toy pool par rapport à la date de disponibilité de l'elfe
        # Avancer jusqu'à ce qu'il y ait des jouets dans l'available list
        while True:
            mytoypool.update_available_toy_list_according_to_elf(elf)
            if mytoypool.length_available_list() > 0:
                break
            else:
                t = elf.get_next_available_time()
                next_t = hrs.next_sanctioned_minute(t)
                elf.set_next_available_time(next_t)


        # Etape 2 : Recupérer la productivité de l'elfe
        productivity = elf.get_productivity()
        
        # Etape 2, Cas 1 : La productivité est supérieure au seuil
        if productivity > PRODUCTIVITY_THRESHOLD:
            # Etape 3 : Récupérer le jouet le plus gros disponible
            toy = mytoypool.get_next_longest_toy_for_elf(elf)

            if toy is not None:
                # Etape 4 : Faire le jouet
                elf.make_toy(toy, wcsv)
            else:
                # On avance d'une minute
                t = elf.get_next_available_time()
                next_t = hrs.next_sanctioned_minute(t)
                elf.set_next_available_time(next_t)

            # Etape 5 : Mettre à jour l'elfe dans le pool d'elfes
            myelfpool.update_elf(elf)

        # Etape 2, Cas 2 : La productivité est inférieure au seuil
        else:

            # Etape 2.2 : Calculer le nombre de minutes restantes avant la fin de la journée
            minutes_left = elf.num_of_working_minutes_left()

            # Etape 3.2 : Avec la productivité, calculer le nombre de minutes max pouvant être consacrées à un jouet
            productivity = elf.get_productivity()
            toy_max_minutes = int(minutes_left*productivity)

            # Ca de rejet
            if toy_max_minutes <= 1:
                # On remet ça à demain
                elf.wait_till_next_day()
                myelfpool.update_elf(elf)
                continue

            # Etape 4.2 : Selectionner un jouet disposant d'un nombre de minutes inférieur à toy_max_minutes
            toy_expected_duration = random.randint(1, toy_max_minutes-1)
            toy = mytoypool.get_toy_by_duration_for_elf(elf, toy_expected_duration)

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
                    toy = mytoypool.get_next_shortest_toy_for_elf(elf)

                    if toy is not None:
                        # Si le temps requis est inférieur au temps restant
                        toy_duration = toy.get_duration()
                        productivity = elf.get_productivity()
                        toy_required_minutes = int(math.ceil(toy_duration / productivity))

                        if toy_required_minutes < minutes_left:
                            # on fait
                            elf.make_toy(toy, wcsv)
                        elif mytoypool.length_waiting_list() <= 900:
                            elf.make_toy(toy, wcsv)
                        else:
                            mytoypool.push_toy_in_available_list(toy)
                            t = elf.get_next_available_time()
                            next_t = hrs.next_sanctioned_minute(t)
                            elf.set_next_available_time(next_t)
                    else:
                        # on passe à la minute suivante
                        t = elf.get_next_available_time()
                        next_t = hrs.next_sanctioned_minute(t)
                        elf.set_next_available_time(next_t)

                    myelfpool.update_elf(elf)
                    
            else:
            # Etape 4.2, Cas 2 : Un tel jouet existe, c'est super on le réalise
                elf.make_toy(toy, wcsv)

                myelfpool.update_elf(elf)



    print 'total runtime = {0}'.format(time.time() - start)
