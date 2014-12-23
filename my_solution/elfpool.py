# -*- coding: utf-8 -*-

import unittest
import heapq
import datetime
from elf import Elf

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


if __name__ == '__main__':
    unittest.main()
