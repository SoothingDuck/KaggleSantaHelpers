# -*- coding: utf-8 -*-

import csv
import unittest
import heapq
import datetime
from elf import Elf
from toy import Toy
from toypool import ToyPool

class ElfPool:

    def __init__(self):
        # Liste des elfes triés par temps de disponibilité
        self.__heap_elf = []

        # Hash date Elf
        self.__hash_elf = {}

    def init_with(self, n):
        """Initialise le pool avec n elfes"""
        for i in range(n):
            self.add_elf(Elf(i+1))

    def __len__(self):
        """Taille du pool"""
        return len(self.__heap_elf)

    def add_elf(self, elf):
        """Ajoute un nouvel elfe dans le pool"""
        # Recupere le timestamp de disponibilité de l'elfe
        next_available_working_time = elf.get_next_available_working_time()

        # Ajoute dans le heap
        heapq.heappush(self.__heap_elf, (next_available_working_time, elf))

    def next_available_elf(self):
        """Retourne le premier elfe disponible"""
        # Retire de la heap
        next_timestamp, elf = heapq.heappop(self.__heap_elf)

        # Retourne l'elfe
        return elf


class ElfPoolTest(unittest.TestCase):

    def setUp(self):
        self.pool = ElfPool()

        self.elf1 = Elf(1, datetime.datetime(2014, 1, 2, 9, 0, 0))
        self.elf2 = Elf(2, datetime.datetime(2014, 1, 2, 9, 10, 0))
        self.pool.add_elf(self.elf1)
        self.pool.add_elf(self.elf2)

    def test_init_with(self):
        self.init_pool = ElfPool()
        self.init_pool.init_with(900)

        self.assertEquals(len(self.init_pool), 900)

    def test_in_out(self):

        elf1 = Elf(1, datetime.datetime(2014, 1, 1, 10, 0))
        elf2 = Elf(2, datetime.datetime(2014, 1, 1, 9, 0))

        elfpool = ElfPool()
        self.assertEquals(len(elfpool), 0)

        elfpool.add_elf(elf1)
        elfpool.add_elf(elf2)

        elf = elfpool.next_available_elf()
        self.assertEquals(len(elfpool), 1)
        self.assertEquals(elf, elf2)

        elf.set_next_available_working_time(datetime.datetime(2014, 1, 1, 11, 0))

        elfpool.add_elf(elf)

        self.assertEquals(len(elfpool), 2)

        self.assertEquals(elfpool.next_available_elf(), elf1)
        self.assertEquals(elfpool.next_available_elf(), elf2)



    def test_next_available_elf(self):
        self.assertEquals(len(self.pool), 2)
        # elf1 est le prochain elfe disponible
        next_available_elf = self.pool.next_available_elf()
        self.assertEquals(next_available_elf, self.elf1)
        self.assertEquals(len(self.pool), 1)

    def test_apply_strategy_for_1(self):
        # CSV
        w = open("test_apply_strategy_for_1.csv", 'wb')
        wcsv = csv.writer(w)
        wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])

        # ElfPool
        elfpool = ElfPool()
        elf1 = Elf(1, datetime.datetime(2014, 1, 1, 9, 0, 0))
        elf2 = Elf(2, datetime.datetime(2014, 1, 1, 9, 5, 0))

        elfpool.add_elf(elf1)
        elfpool.add_elf(elf2)

        # ToyPool
        toypool = ToyPool()
        toy1 = Toy(1, "2014 1 1 8 0", 10)
        toy2 = Toy(2, "2014 1 1 10 0", 10)

        toypool.append(toy1)
        toypool.append(toy2)

        # Strategy
        elf = elfpool.next_available_elf()
        elf.apply_strategy_for(toypool, elfpool, wcsv)
        elfpool.add_elf(elf)

        # Tests
        e2 = elfpool.next_available_elf()
        e1 = elfpool.next_available_elf()

        self.assertEquals(e1, elf1)
        self.assertEquals(e2, elf2)

        self.assertEquals(e1.get_next_available_working_time(), datetime.datetime(2014, 1, 1, 9, 10))
        self.assertEquals(e2.get_next_available_working_time(), datetime.datetime(2014, 1, 1, 9, 5))

        self.assertEquals(len(toypool), 1)

        self.assertTrue(datetime.datetime(2014, 1, 1, 10, 0) in toypool.get_known_timestamp_list())
        self.assertTrue(toypool.get_hash_count().has_key(datetime.datetime(2014, 1, 1, 10, 0)))

        self.assertTrue(toypool.toy_exists_in_pool(toy2))

    def test_apply_strategy_for_2(self):
        # CSV
        w = open("test_apply_strategy_for_2.csv", 'wb')
        wcsv = csv.writer(w)
        wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])

        # ElfPool
        elfpool = ElfPool()
        elf1 = Elf(1, datetime.datetime(2014, 1, 1, 9, 0, 0))
        elf2 = Elf(2, datetime.datetime(2014, 1, 1, 9, 5, 0))

        elfpool.add_elf(elf1)
        elfpool.add_elf(elf2)

        # ToyPool
        toypool = ToyPool()
        toy1 = Toy(1, "2014 1 1 8 0", 900)
        toy2 = Toy(2, "2014 1 1 10 0", 10)

        toypool.append(toy1)
        toypool.append(toy2)

        print toy1
        print toy2

        # Strategy
        elf = elfpool.next_available_elf()
        elf.apply_strategy_for(toypool, elfpool, wcsv)
        elfpool.add_elf(elf)

        # Tests
        e2 = elfpool.next_available_elf()
        e1 = elfpool.next_available_elf()

        print e1
        print e2

        print elf1
        print elf2

        self.assertEquals(e1, elf1)
        self.assertEquals(e2, elf2)

        self.assertEquals(e1.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 14, 0))
        self.assertEquals(e2.get_next_available_working_time(), datetime.datetime(2014, 1, 1, 9, 5))

        self.assertEquals(len(toypool), 1)

        self.assertTrue(datetime.datetime(2014, 1, 1, 10, 0) in toypool.get_known_timestamp_list())
        self.assertTrue(toypool.get_hash_count().has_key(datetime.datetime(2014, 1, 1, 10, 0)))

        self.assertTrue(toypool.toy_exists_in_pool(toy2))

    def test_apply_strategy_for_3(self):
        # CSV
        w = open("test_apply_strategy_for_3.csv", 'wb')
        wcsv = csv.writer(w)
        wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])

        # ElfPool
        elfpool = ElfPool()
        elf1 = Elf(1, datetime.datetime(2014, 1, 1, 9, 0, 0))

        elfpool.add_elf(elf1)

        # ToyPool
        toypool = ToyPool()
        toy1 = Toy(1, "2014 1 1 8 0", 900)
        toy2 = Toy(2, "2014 1 1 10 0", 10)

        toypool.append(toy1)
        toypool.append(toy2)

        # Strategy
        elf = elfpool.next_available_elf()
        elf.apply_strategy_for(toypool, elfpool, wcsv)
        elfpool.add_elf(elf)

        elf = elfpool.next_available_elf()
        elf.apply_strategy_for(toypool, elfpool, wcsv)
        elfpool.add_elf(elf)

        # Tests
        e = elfpool.next_available_elf()

        self.assertEquals(e.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 14, 14))

        self.assertEquals(len(toypool), 0)

    def test_available_list(self):

        elfpool = ElfPool()
        elf1 = Elf(1, datetime.datetime(2014, 1, 1, 9, 0))
        elf2 = Elf(2, datetime.datetime(2014, 1, 1, 10, 0))
        elfpool.add_elf(elf1)
        elfpool.add_elf(elf2)

        toypool = ToyPool()

        toy1 = Toy(1, "2014 1 1 8 5", 600)
        toy2 = Toy(2, "2014 1 1 9 6", 60)

        toypool.push_toy_in_waiting_list(toy1)
        toypool.push_toy_in_waiting_list(toy2)

        self.assertEquals(toypool.length_waiting_list(), 2)
        self.assertEquals(toypool.length_available_list(), 0)

        toypool.fill_available_list_according_to(elfpool)

        self.assertEquals(toypool.length_waiting_list(), 1)
        self.assertEquals(toypool.length_available_list(), 1)

        toy = toypool.pop_next_available_toy()

        self.assertEquals(toy, toy1)

        self.assertEquals(toypool.length_waiting_list(), 1)
        self.assertEquals(toypool.length_available_list(), 0)

        toypool.push_in_available_list_toy(toy)

        self.assertEquals(toypool.length_waiting_list(), 1)
        self.assertEquals(toypool.length_available_list(), 1)

        toy = toypool.pop_next_available_toy()

        self.assertEquals(toypool.length_waiting_list(), 1)
        self.assertEquals(toypool.length_available_list(), 0)

        toypool.fill_available_list_according_to(elfpool)

        self.assertEquals(toypool.length_waiting_list(), 0)
        self.assertEquals(toypool.length_available_list(), 1)

        toy = toypool.pop_next_available_toy()

        self.assertEquals(toy, toy2)


if __name__ == '__main__':
    unittest.main()
