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

    def fill_available_list_according_to(self, elfpool):
        """Mets à jour l'available list avec les jouets disponibles"""
        elf_list = []

        elf = elfpool.next_available_elf()
        elf_list.append(elf)

        while True:
            toy = self.pop_toy_of_waiting_list()
            toy_timestamp = toy.get_min_possible_working_start_time()
            if toy_timestamp <= elf_timestamp:
                self.push_toy_in_available_list(toy)
            else:
                self.push_toy_in_waiting_list(toy)
                break

    def pop_toy_of_waiting_list(self):
        """Retourne le prochain jouet de la waiting list"""
        toy_timestamp, toy = heapq.heappop(self.__waiting_list)
        return toy

    def toy_exists_in_pool(self, toy):
        """Test l'existence du jouet dans la file"""
        return self.__hash_existence_by_id.has_key(toy.id)
 
    def get_hash_count(self):
        """Retourne le hash count"""
        return self.__hash_count

    def get_hash_existence_by_id(self):
        """Retourne le hash d'existence"""
        return self.__hash_existence_by_id

    def __init__(self):

        # waiting list
        self.__waiting_list = []

        # available list
        self.__available_list = []

    def __len__(self):
        """Retourne la taille du toy pool"""
        return self.__toy_counter

    def toy_left_for_elf(self, elf):
        """Il reste des jouets pour l'elfe"""
        next_working_time = elf.get_next_available_working_time()
        return (next_working_time >= self.__known_timestamp_list[0])

    def get_random_toy_for_elf(self, elf):
        """Retourne un jouet au hasard disponible pour l'elf"""

        # Loop tant qu'on n'a rien de disponible
        while not self.toy_left_for_elf(elf):
            elf.tick_to_next_minute()

        # Timestamp de l'elfe
        elf_timestamp = elf.get_next_available_working_time()

        # Indice max de la liste des timestamp
        imax = bisect.bisect_right(self.__known_timestamp_list, elf_timestamp)

        # Indice au hasard
        try:
            i = random.randint(0, imax-1)
        except:
            print(imax)
            print(elf_timestamp, self.__known_timestamp_list)
            raise

        # Recuperation du timestamp
        toy_timestamp = self.__known_timestamp_list[i]

        # Recuperation du jouet dans la random heap
        while True:
            r, toy = heapq.heappop(self.__hash_random_heap_by_timestamp[toy_timestamp])
            if self.__hash_existence_by_id.has_key(toy.id):
                break

        # Suppression de l'existence hash
        del self.__hash_existence_by_id[toy.id]

        # Decrement counter
        self.__hash_count[toy_timestamp] -= 1

        # Mise à zero des élements
        if self.__hash_count[toy_timestamp] == 0:
            del self.__hash_count[toy_timestamp]
            del self.__hash_random_heap_by_timestamp[toy_timestamp]
            del self.__hash_duration_heap_by_timestamp[toy_timestamp]
            del self.__known_timestamp_list[i]

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

    def append_hash_count_by_timestamp(self, toy):
        """Met à jour le hash"""
        toy_timestamp = toy.get_min_possible_working_start_time()

        if not self.__hash_count.has_key(toy_timestamp):
            self.__hash_count[toy_timestamp] = 0

        self.__hash_count[toy_timestamp] += 1

    def append_hash_duration_heap_by_timestamp(self, toy):
        """Met à jour le hash"""
        toy_timestamp = toy.get_min_possible_working_start_time()
        toy_duration = toy.get_duration()

        if not self.__hash_duration_heap_by_timestamp.has_key(toy_timestamp):
            self.__hash_duration_heap_by_timestamp[toy_timestamp] = []

        heapq.heappush(self.__hash_duration_heap_by_timestamp[toy_timestamp], (toy_duration, toy))

    def append_hash_random_heap_by_timestamp(self, toy):
        """Met à jour le hash"""
        toy_timestamp = toy.get_min_possible_working_start_time()

        if not self.__hash_random_heap_by_timestamp.has_key(toy_timestamp):
            self.__hash_random_heap_by_timestamp[toy_timestamp] = []

        r = random.random()
        heapq.heappush(self.__hash_random_heap_by_timestamp[toy_timestamp], (r, toy))

    def push_toy_in_waiting_list(self, toy):
        """Ajoute un jouet dans la liste"""
        # Regarde le timestamp minimum à partir duquel un elfe pourrait travailler sur le jouet
        toy_timestamp = toy.get_min_possible_working_start_time()

        # Mets à jour la waiting list
        heapq.heappush(self.__waiting_list, (toy_timestamp, toy))

    def length_available_list(self):
        """Retourne la taille de la waiting list"""
        return len(self.__available_list)

    def length_waiting_list(self):
        """Retourne la taille de la waiting list"""
        return len(self.__waiting_list)

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


from elfpool import ElfPool

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


    def test_toy_left_for_elf(self):

        elf = Elf(1, datetime.datetime(2014, 1, 1, 9, 5, 0))

        pool = ToyPool()

        toy1 = Toy(1, "2014 1 1 9 5", 600)
        toy2 = Toy(2, "2014 1 1 9 6", 60)

        pool.append(toy1)
        pool.append(toy2)

        self.assertTrue(pool.toy_left_for_elf(elf))

    def test_empty(self):
        self.assertTrue(self.toy_empty_pool.empty())


    def test_get_random_toy_for_elf(self):
        """Jouet au hasard parmi ceux disponibles"""
        self.assertEquals(len(self.toy_small_pool), 3)

        # Recupere un jouet au hasard => seul le 1 est disponible
        random_toy = self.toy_small_pool.get_random_toy_for_elf(self.elf)  

        self.assertTrue(random_toy not in (self.toy2, self.toy3))
        self.assertEquals(random_toy, self.toy1)

        self.assertEquals(len(self.toy_small_pool), 2)


if __name__ == '__main__':
    unittest.main()

