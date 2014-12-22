# -*- coding: utf-8 -*-

import os
import csv
import heapq
import bisect
import unittest
import datetime
import random

from toy import Toy
from elf import Elf

class ToyPool:
    """List of Toys to make"""

    def __init__(self):

        # List of known timestamp
        self.__known_timestamp_list = []

        # Hash of timestamp and heap of toys ordered by duration
        self.__hash_timestamp_toys = {}

        # Nb of toys
        self.__toy_counter = 0

    def __len__(self):
        """Retourne la taille du toy pool"""
        return self.__toy_counter

    def get_random_toy_for_elf(self, elf):
        """Retourne un jouet au hasard disponible pour l'elf"""
        # Timestamp de l'elfe
        elf_timestamp = elf.get_next_available_working_time()

        # Indice max de la liste des timestamp
        imax = bisect.bisect_right(self.__known_timestamp_list, elf_timestamp)

        # Indice au hasard
        i = random.randint(0, imax-1)

        # Recuperation du timestamp
        toy_timestamp = self.__known_timestamp_list[i]

        # Recuperation d'un indice de jouet au hasard
        toy_indice = random.randint(0, len(self.__hash_timestamp_toys[toy_timestamp])-1) 

        # Recuperation du jouet
        duration, toy = self.__hash_timestamp_toys[toy_timestamp].pop(toy_indice)

        # Cas 1 : la liste est vide
        if len(self.__hash_timestamp_toys[toy_timestamp]) == 0:
            del self.__hash_timestamp_toys[toy_timestamp]
            del self.__known_timestamp_list[i]
        else:
        # Cas 2 : Reheap
            heapq.heapify(self.__hash_timestamp_toys[toy_timestamp])

        # Mise à jour du compteur
        self.__toy_counter -= 1

        # On retourne le jouet
        return toy


    def empty(self):
        """Retourne True si la liste est vide"""
        return len(self.__known_timestamp_list) == 0
    
    def get_known_timestamp_list(self):
        """Retourne la liste des timestamp contenant des objets"""
        return(self.__known_timestamp_list)

    def append_known_timestamp_list_with_toy_timestamp(self, toy_timestamp):
        """Met à jour la liste des timestamp"""
        # Binary search du timestamp
        i = bisect.bisect_left(self.__known_timestamp_list, toy_timestamp)

        if i != len(self.__known_timestamp_list) and self.__known_timestamp_list[i] == toy_timestamp:
            # L'indice est présent
            return
        else:
            # Sinon
            self.__known_timestamp_list.insert(i, toy_timestamp)

    def append_hash_timestamp_toys_with(self, toy_timestamp, toy):
        """Met à jour le hash"""
        if not self.__hash_timestamp_toys.has_key(toy_timestamp):
            self.__hash_timestamp_toys[toy_timestamp] = []

        toy_duration = toy.get_duration()
        heapq.heappush(self.__hash_timestamp_toys[toy_timestamp], (toy_duration, toy))

    def append(self, toy):
        """Ajoute un jouet dans la liste"""
        # Regarde le timestamp minimum à partir duquel un elfe pourrait travailler sur le jouet
        toy_timestamp = toy.get_min_possible_working_start_time()

        # Met à jour la liste des known timestamp si necessaire
        self.append_known_timestamp_list_with_toy_timestamp(toy_timestamp)

        # Met à jour le hash avec la queue correspondante
        self.append_hash_timestamp_toys_with(toy_timestamp, toy)

        # Met à jour le toy counter
        self.__toy_counter += 1


    def add_file_content(self, toy_file, num_toys=None):
        """Ajout de jouets Ã  partir d'un fichier"""
        i = 0
        with open(toy_file, 'rb') as f:
            fcsv = csv.reader(f)
            fcsv.next()  # header row
            for row in fcsv:
                i += 1
                new_toy = Toy(row[0], row[1], row[2])
                self.append(new_toy)
                if len(self) % 1000 == 0:
                    print len(self)

                if num_toys is not None and i >= num_toys:
                    break

        if num_toys is not None and len(self) != num_toys:
            print '\n ** Read a file with {0} toys, expected {1} toys. Exiting.'.format(len(self), num_toys)
            exit(-1)

class ToyPoolTest(unittest.TestCase):

    def setUp(self):
        toy_file = os.path.join(os.getcwd(), '..', 'DATA', 'toys_rev2.csv')
        self.toy_empty_pool = ToyPool()
        self.toy_filled_pool = ToyPool()
        self.toy_filled_pool.add_file_content(toy_file, 10)

        self.elf = Elf(1, datetime.datetime(2014, 1, 1, 9, 0, 0))
        self.toy_small_pool = ToyPool()
        self.toy1 = Toy(1, "2014 1 1 8 0", 600)
        self.toy2 = Toy(2, "2014 1 1 9 3", 60)
        self.toy3 = Toy(3, "2014 1 1 10 0", 2)
        self.toy_small_pool.append(self.toy1)
        self.toy_small_pool.append(self.toy2)
        self.toy_small_pool.append(self.toy3)


    def test_empty(self):
        self.assertTrue(self.toy_empty_pool.empty())


    def test_get_random_toy_for_elf(self):
        """Jouet au hasard parmi ceux disponibles"""
        self.assertEquals(len(self.toy_small_pool), 3)

        random_toy = self.toy_small_pool.get_random_toy_for_elf(self.elf)  

        self.assertTrue(random_toy not in (self.toy2, self.toy3))
        self.assertEquals(random_toy, self.toy1)

        self.assertEquals(len(self.toy_small_pool), 2)


if __name__ == '__main__':
    unittest.main()

