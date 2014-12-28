# -*- coding: utf-8 -*-

import csv
import unittest
import heapq
import datetime
from elf import Elf
from toy import Toy
from toypool import ToyPool

class ElfPool:

    def __init__(self, n):
        # Liste des elfes triés par temps de disponibilité
        self.__hash_elf = {}
        for i in range(n):
            self.__hash_elf[i+1] = Elf(i+1)

    def __len__(self):
        """Taille du pool"""
        return len(self.__hash_elf)

    def all_elves_next_available_working_time(self):
        """Recupere l'ensemble des next available working time"""
        return [x.get_next_available_working_time() for x in self.__hash_elf.values()]

    def min_next_available_working_time_among_elves(self):
        """Retourne le min next available working time"""
        return min(self.all_elves_next_available_working_time())

    def max_next_available_working_time_among_elves(self):
        """Retourne le max next available working time"""
        return max(self.all_elves_next_available_working_time())

    def update_elf(self, elf):
        """Mets à jour un elfe dans le pool"""
        # Mets à jour dans le hash
        self.__hash_elf[elf.id] = elf

    def elf_list(self):
        """Retourne la liste des elfes"""
        return self.__hash_elf.values()

class ElfPoolTest(unittest.TestCase):

    def setUp(self):
        self.pool = ElfPool(2)

        self.elf1 = Elf(1, datetime.datetime(2014, 1, 2, 9, 0, 0))
        self.elf2 = Elf(2, datetime.datetime(2014, 1, 2, 9, 10, 0))
        self.pool.update_elf(self.elf1)
        self.pool.update_elf(self.elf2)

    def test_init_with(self):
        self.init_pool = ElfPool(900)

        self.assertEquals(len(self.init_pool), 900)

    def test_in_out(self):

        elf1 = Elf(1, datetime.datetime(2014, 1, 1, 10, 0))
        elf2 = Elf(2, datetime.datetime(2014, 1, 1, 9, 0))

        elfpool = ElfPool(2)
        self.assertEquals(len(elfpool), 2)

        elfpool.update_elf(elf1)
        elfpool.update_elf(elf2)

        elf = elfpool.next_available_elf()
        self.assertEquals(elf, elf2)

        elf.set_next_available_working_time(datetime.datetime(2014, 1, 1, 11, 0))

        elfpool.update_elf(elf)

        self.assertEquals(elfpool.next_available_elf(), elf1)



    def test_next_available_elf(self):
        self.assertEquals(len(self.pool), 2)
        # elf1 est le prochain elfe disponible
        next_available_elf = self.pool.next_available_elf()
        self.assertEquals(next_available_elf, self.elf1)
        self.assertEquals(len(self.pool), 1)

#     def test_apply_strategy_for_1(self):
#         # CSV
#         w = open("test_apply_strategy_for_1.csv", 'wb')
#         wcsv = csv.writer(w)
#         wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])
# 
#         # ElfPool
#         elfpool = ElfPool()
#         elf1 = Elf(1, datetime.datetime(2014, 1, 1, 9, 0, 0))
#         elf2 = Elf(2, datetime.datetime(2014, 1, 1, 9, 5, 0))
# 
#         elfpool.add_elf(elf1)
#         elfpool.add_elf(elf2)
# 
#         # ToyPool
#         toypool = ToyPool()
#         toy1 = Toy(1, "2014 1 1 8 0", 10)
#         toy2 = Toy(2, "2014 1 1 10 0", 10)
# 
#         toypool.append(toy1)
#         toypool.append(toy2)
# 
#         # Strategy
#         elf = elfpool.next_available_elf()
#         elf.apply_strategy_for(toypool, elfpool, wcsv)
#         elfpool.add_elf(elf)
# 
#         # Tests
#         e2 = elfpool.next_available_elf()
#         e1 = elfpool.next_available_elf()
# 
#         self.assertEquals(e1, elf1)
#         self.assertEquals(e2, elf2)
# 
#         self.assertEquals(e1.get_next_available_working_time(), datetime.datetime(2014, 1, 1, 9, 10))
#         self.assertEquals(e2.get_next_available_working_time(), datetime.datetime(2014, 1, 1, 9, 5))
# 
#         self.assertEquals(len(toypool), 1)
# 
#         self.assertTrue(datetime.datetime(2014, 1, 1, 10, 0) in toypool.get_known_timestamp_list())
#         self.assertTrue(toypool.get_hash_count().has_key(datetime.datetime(2014, 1, 1, 10, 0)))
# 
#         self.assertTrue(toypool.toy_exists_in_pool(toy2))
# 
#     def test_apply_strategy_for_2(self):
#         # CSV
#         w = open("test_apply_strategy_for_2.csv", 'wb')
#         wcsv = csv.writer(w)
#         wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])
# 
#         # ElfPool
#         elfpool = ElfPool()
#         elf1 = Elf(1, datetime.datetime(2014, 1, 1, 9, 0, 0))
#         elf2 = Elf(2, datetime.datetime(2014, 1, 1, 9, 5, 0))
# 
#         elfpool.add_elf(elf1)
#         elfpool.add_elf(elf2)
# 
#         # ToyPool
#         toypool = ToyPool()
#         toy1 = Toy(1, "2014 1 1 8 0", 900)
#         toy2 = Toy(2, "2014 1 1 10 0", 10)
# 
#         toypool.append(toy1)
#         toypool.append(toy2)
# 
#         print toy1
#         print toy2
# 
#         # Strategy
#         elf = elfpool.next_available_elf()
#         elf.apply_strategy_for(toypool, elfpool, wcsv)
#         elfpool.add_elf(elf)
# 
#         # Tests
#         e2 = elfpool.next_available_elf()
#         e1 = elfpool.next_available_elf()
# 
#         print e1
#         print e2
# 
#         print elf1
#         print elf2
# 
#         self.assertEquals(e1, elf1)
#         self.assertEquals(e2, elf2)
# 
#         self.assertEquals(e1.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 14, 0))
#         self.assertEquals(e2.get_next_available_working_time(), datetime.datetime(2014, 1, 1, 9, 5))
# 
#         self.assertEquals(len(toypool), 1)
# 
#         self.assertTrue(datetime.datetime(2014, 1, 1, 10, 0) in toypool.get_known_timestamp_list())
#         self.assertTrue(toypool.get_hash_count().has_key(datetime.datetime(2014, 1, 1, 10, 0)))
# 
#         self.assertTrue(toypool.toy_exists_in_pool(toy2))
# 
#     def test_apply_strategy_for_3(self):
#         # CSV
#         w = open("test_apply_strategy_for_3.csv", 'wb')
#         wcsv = csv.writer(w)
#         wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])
# 
#         # ElfPool
#         elfpool = ElfPool()
#         elf1 = Elf(1, datetime.datetime(2014, 1, 1, 9, 0, 0))
# 
#         elfpool.add_elf(elf1)
# 
#         # ToyPool
#         toypool = ToyPool()
#         toy1 = Toy(1, "2014 1 1 8 0", 900)
#         toy2 = Toy(2, "2014 1 1 10 0", 10)
# 
#         toypool.append(toy1)
#         toypool.append(toy2)
# 
#         # Strategy
#         elf = elfpool.next_available_elf()
#         elf.apply_strategy_for(toypool, elfpool, wcsv)
#         elfpool.add_elf(elf)
# 
#         elf = elfpool.next_available_elf()
#         elf.apply_strategy_for(toypool, elfpool, wcsv)
#         elfpool.add_elf(elf)
# 
#         # Tests
#         e = elfpool.next_available_elf()
# 
#         self.assertEquals(e.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 14, 14))
# 
#         self.assertEquals(len(toypool), 0)

    def test_available_list(self):

        elfpool = ElfPool(3)
        elf1 = Elf(1, datetime.datetime(2014, 1, 1, 9, 0))
        elf2 = Elf(2, datetime.datetime(2014, 1, 1, 10, 0))
        elf3 = Elf(3, datetime.datetime(2014, 1, 1, 15, 0))
        elfpool.add_elf(elf1)
        elfpool.add_elf(elf2)
        elfpool.add_elf(elf3)

        toypool = ToyPool()

        toy1 = Toy(1, "2014 1 1 8 5", 600)
        toy2 = Toy(2, "2014 1 1 9 6", 60)
        toy3 = Toy(3, "2014 1 1 12 6", 60)

        toypool.push_toy_in_waiting_list(toy1)
        toypool.push_toy_in_waiting_list(toy2)
        toypool.push_toy_in_waiting_list(toy3)

        self.assertEquals(toypool.length_waiting_list(), 3)
        self.assertEquals(toypool.length_available_list(), 0)

        toypool.fill_available_list_according_to(elfpool)

        self.assertEquals(toypool.length_waiting_list(), 2)
        self.assertEquals(toypool.length_available_list(), 1)

        toy = toypool.pop_toy_of_available_list()

        self.assertEquals(toy, toy1)

        self.assertEquals(toypool.length_waiting_list(), 2)
        self.assertEquals(toypool.length_available_list(), 0)

        toypool.push_toy_in_available_list(toy)

        self.assertEquals(toypool.length_waiting_list(), 2)
        self.assertEquals(toypool.length_available_list(), 1)

        toy = toypool.pop_toy_of_available_list()

        self.assertEquals(toypool.length_waiting_list(), 2)
        self.assertEquals(toypool.length_available_list(), 0)

        toypool.fill_available_list_according_to(elfpool)

        self.assertEquals(toypool.length_waiting_list(), 1)
        self.assertEquals(toypool.length_available_list(), 1)

        toy = toypool.pop_toy_of_available_list()

        self.assertEquals(toy, toy2)

        toypool.fill_available_list_according_to(elfpool)

        self.assertEquals(len(elfpool), 3)

        self.assertEquals(toypool.length_waiting_list(), 0)
        self.assertEquals(toypool.length_available_list(), 1)

if __name__ == '__main__':
    unittest.main()
