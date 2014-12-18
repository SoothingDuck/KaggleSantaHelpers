# -*- coding: utf-8 -*-

import os
import csv
import heapq
import bisect
import unittest

from toy import Toy
from elf import Elf

class ToyPool:

    def __init__(self):

        # Heap de base
        self.__base_heap = []

        # Liste tri�e par timestamp pour la recherche random
        self.__sorted_toys_for_random_search = []

        # Hash par timestamp avec heap ordonné par duration
        self.__timestamp_hash_toy_heap = {}

        # Liste ordonnée référencant les timestamp pour lesquels on a des jouets
        self.__known_timestamps = []

    def __len__(self):
        """Retourne le nombre de jouets présents dans le pool"""
        return len(self.__base_heap)

    def push(self, toy, unsorted=False):
        """Ajoute un jouet dans la liste"""
        # get timestamp for toy
        toy_timestamp = toy.get_min_possible_working_start_time()
        toy_duration = toy.get_toy_duration()
        
        # add to heap
        heapq.heappush(self.__base_heap, (toy_timestamp, toy))

        # add to list for random search
        if unsorted:
            # set sorted status to false
            self.__random_search_sorted = False
            self.__sorted_toys_for_random_search.append((toy_timestamp, toy))
        else:
            bisect.insort_left(self.__sorted_toys_for_random_search, (toy_timestamp, toy))
        
        # Insert into timestamp hash
        if not self.__timestamp_hash_toy_heap.has_key(toy_timestamp):
            self.__timestamp_hash_toy_heap[toy_timestamp] = []
            bisect.insort_right(self.__known_timestamps, toy_timestamp)

        heapq.heappush(self.__timestamp_hash_toy_heap[toy_timestamp], (toy_duration, toy))

    def __sort_toypool_if_not_sorted(self):
        if not self.__sorted_toys_for_random_search:
            self.__sorted_toys_for_random_search.sort()

    def pop(self):
        """Enl�ve un jouet de la pile"""
        # add to heap
        toy_timestamp, toy = heapq.heappop(self.__base_heap)

        # add to list for random search
        self.__sort_toypool_if_not_sorted()


        i = bisect.bisect(self.__sorted_toys_for_random_search, (toy_timestamp, toy))
        del self.__sorted_toys_for_random_search[i-1]
        
        # Insert into timestamp hash
        heapq.heappop(self.__timestamp_hash_toy_heap[toy_timestamp])

        # On retourne le jouet
        return toy

    def add_file_content(self, toy_file, num_toys=None):
        """Ajout de jouets à partir d'un fichier"""
        i = 0
        with open(toy_file, 'rb') as f:
            fcsv = csv.reader(f)
            fcsv.next()  # header row
            for row in fcsv:
                i += 1
                new_toy = Toy(row[0], row[1], row[2])
                self.push(new_toy)
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


    def test_len(self):
        self.assertEqual(len(self.toy_filled_pool), 10)

    def test_push_pop(self):
        toy1 = Toy(1, "2014 1 1 8 0", 50)
        toy2 = Toy(2, "2014 1 1 10 30", 20)
        toy3 = Toy(3, "2014 1 1 19 30", 10)

        self.toy_empty_pool.push(toy1)
        self.toy_empty_pool.push(toy2)
        self.toy_empty_pool.push(toy3)

        self.assertEqual(self.toy_empty_pool.pop(), toy1)
        self.assertEqual(self.toy_empty_pool.pop(), toy2)
        self.assertEqual(self.toy_empty_pool.pop(), toy3)

    def test_pop_random_toy_for_elf(self):
        elf = Elf(1)
        elf.set_next_available_time(datetime.datetime(2014, 1, 1, 11, 40))

        self.assertEqual(elf.get_available_time_in_minutes(), (11*60)+40)

        toy1 = Toy(1, "2014 1 1 8 0", 50)
        toy2 = Toy(2, "2014 1 1 10 30", 20)
        toy3 = Toy(3, "2014 1 1 19 30", 10)

        self.toy_empty_pool.push(toy1)
        self.toy_empty_pool.push(toy2)
        self.toy_empty_pool.push(toy3)
        
        self.assertIsNotNone(self.toy_empty_pool.pop_random_toy_for_elf(elf))
        self.assertIsNotNone(self.toy_empty_pool.pop_random_toy_for_elf(elf))
        self.assertIsNone(self.toy_empty_pool.pop_random_toy_for_elf(elf))

    def test_pop_least_long_toy_next_to_timestamp_for_elf(self):

        elf = Elf(1)
        elf.set_next_available_time(datetime.datetime(2014, 1, 1, 11, 40))

        toy1 = Toy(1, "2014 1 1 8 0", 50)
        toy2 = Toy(2, "2014 1 1 10 30", 30)
        toy3 = Toy(2, "2014 1 1 10 30", 20)
        toy4 = Toy(3, "2014 1 1 19 30", 10)

        self.toy_empty_pool.push(toy1)
        self.toy_empty_pool.push(toy2)
        self.toy_empty_pool.push(toy3)
        self.toy_empty_pool.push(toy4)

        self.assertEqual(self.toy_empty_pool.pop_least_long_toy_next_to_timestamp_for_elf(elf), toy3)


if __name__ == '__main__':
    unittest.main()

