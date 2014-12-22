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

    def empty_for_date(self, thedate):
        """Valide si des elfes sont disponibles pour une date donnée"""
        for pool_date in self.__hash_elf.keys():
            if pool_date <= thedate:
                return False

        return True

    def add_elf(self, elf):
        """Ajoute un nouvel elfe dans le pool"""
        # Recupere le timestamp de disponibilité de l'elfe
        next_available_working_time = elf.get_next_available_working_time()

        # Ajoute dans le heap
        heapq.heappush(self.__heap_elf, (next_available_working_time, elf))

        # Ajoute dans le hash 
        working_date = next_available_working_time.date()
        if not self.__hash_elf.has_key(working_date):
            self.__hash_elf[working_date] = []

        self.__hash_elf[working_date].append(elf)

    def next_available_elf(self):
        """Retourne le premier elfe disponible"""
        # Retire de la heap
        next_timestamp, elf = heapq.heappop(self.__heap_elf)

        # Retire du hash
        next_date = next_timestamp.date()
        self.__hash_elf[next_date].pop(self.__hash_elf[next_date].index(elf))

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

    def test_empty_for_working_date(self):
        # Y-a-t-il des elfes ou non disponibles avant cette date
        self.assertTrue(self.pool.empty_for_date(datetime.date(2014, 1, 1)))
        self.assertFalse(self.pool.empty_for_date(datetime.date(2014, 1, 2)))
        self.assertFalse(self.pool.empty_for_date(datetime.date(2014, 1, 3)))

    def test_next_available_elf(self):
        self.assertEquals(len(self.pool), 2)
        # elf1 est le prochain elfe disponible
        next_available_elf = self.pool.next_available_elf()
        self.assertEquals(next_available_elf, self.elf1)
        self.assertEquals(len(self.pool), 1)


if __name__ == '__main__':
    unittest.main()
