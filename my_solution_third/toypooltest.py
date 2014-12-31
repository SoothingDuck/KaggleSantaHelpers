# -*- coding: utf-8 -*-

import unittest
import os

from toypool import ToyPool
from elfpool import ElfPool
from elf import Elf
from toy import Toy

class ToyPoolTest(unittest.TestCase):

    def setUp(self):
        toy_file = os.path.join(os.getcwd(), '..', 'DATA', 'toys_rev2.csv')
        self.toy_empty_pool = ToyPool()
        self.toy_filled_pool = ToyPool()
        self.toy_filled_pool.add_file_content(toy_file, 10)

        self.elf = Elf(1)
        self.toy_small_pool = ToyPool()
        self.toy1 = Toy(1, "2014 1 1 8 0", 600)
        self.toy2 = Toy(2, "2014 1 1 9 3", 60)
        self.toy3 = Toy(3, "2014 1 1 10 0", 2)
        self.toy4 = Toy(4, "2014 1 1 9 5", 60)
        self.toy_small_pool.push_toy_in_waiting_list(self.toy1)
        self.toy_small_pool.push_toy_in_waiting_list(self.toy2)
        self.toy_small_pool.push_toy_in_waiting_list(self.toy3)
        self.toy_small_pool.push_toy_in_waiting_list(self.toy4)

    def test_walk_all_durations(self):

        toy_pool = ToyPool()
        toy1 = Toy(1, "2014 1 1 9 5", 30)
        toy2 = Toy(2, "2014 1 1 10 5", 20)
        toy3 = Toy(3, "2014 1 1 8 5", 10)
        toy_pool.push_toy_in_waiting_list(toy1)
        toy_pool.push_toy_in_waiting_list(toy2)
        toy_pool.push_toy_in_waiting_list(toy3)

        elf_pool = ElfPool(2)

        elf1 = elf_pool.next_available_elf()
        toy_pool.update_available_toy_list_according_to_elf(elf1) # 1 et 2 dans available

        # On prends un 31
        toy = toy_pool.get_toy_by_duration(30)
        self.assertEquals(toy, toy3)

    def test_behaviour(self):

        toy_pool = ToyPool()
        toy1 = Toy(1, "2014 1 1 9 5", 20)
        toy2 = Toy(2, "2014 1 1 8 5", 30)
        toy3 = Toy(3, "2014 1 1 8 3", 15)
        toy_pool.push_toy_in_waiting_list(toy1)
        toy_pool.push_toy_in_waiting_list(toy2)
        toy_pool.push_toy_in_waiting_list(toy3)

        elf_pool = ElfPool(2)

        elf1 = elf_pool.next_available_elf()

        toy_pool.update_available_toy_list_according_to_elf(elf1) # 1 et 2 dans available

        # on essaye de prendre un duration 10
        toy = toy_pool.get_toy_by_duration(10)
        self.assertTrue(toy is None)

        # on essaye de prendre un duration 30
        toy = toy_pool.get_toy_by_duration(30)
        self.assertEquals(toy, toy2)

        # on pousse l'elfe au lendemain
        elf1.wait_till_next_day()

        # on mets à jour
        toy_pool.update_available_toy_list_according_to_elf(elf1)

        # changment d'elfe
        elf2 = elf_pool.next_available_elf()

        # On essaye de prendre un duration 17
        toy = toy_pool.get_toy_by_duration(17)
        self.assertTrue(toy is None)

        # On essaye de prendre un duration 21
        toy = toy_pool.get_toy_by_duration(21)
        self.assertEquals(toy, toy1)

    def test_get_next_shortest_toy(self):

        self.elf.wait_till_next_day()
        self.toy_small_pool.update_available_toy_list_according_to_elf(self.elf)

        self.assertEquals(self.toy_small_pool.length_waiting_list(), 0)
        self.assertEquals(self.toy_small_pool.length_available_list(), 4)

        toy = self.toy_small_pool.get_next_shortest_toy()

        self.assertEquals(toy, self.toy3)

        self.assertEquals(self.toy_small_pool.length_waiting_list(), 0)
        self.assertEquals(self.toy_small_pool.length_available_list(), 3)

        toy = self.toy_small_pool.get_next_shortest_toy()
        self.assertEquals(toy.get_duration(), 60)

        toy = self.toy_small_pool.get_next_shortest_toy()
        self.assertEquals(toy.get_duration(), 60)

        toy = self.toy_small_pool.get_next_shortest_toy()
        self.assertEquals(toy.get_duration(), 600)

        toy = self.toy_small_pool.get_next_shortest_toy()
        self.assertTrue(toy is None)

    def test_push_toy_in_available_list(self):

        self.assertEquals(self.toy_small_pool.length_waiting_list(), 4)
        self.assertEquals(self.toy_small_pool.length_available_list(), 0)

        toy_timestamp, toy = self.toy_small_pool.pop_toy_from_waiting_list()

        self.toy_small_pool.push_toy_in_available_list(toy)
        
        self.assertEquals(self.toy_small_pool.length_waiting_list(), 3)
        self.assertEquals(self.toy_small_pool.length_available_list(), 1)

        self.assertEquals(self.toy_small_pool.get_available_toy_duration(), [600])
        self.assertEquals(self.toy_small_pool.get_available_toy_hash(), { 600 : [self.toy1] })

        self.assertTrue(self.toy_small_pool.has_available_toy(self.toy1))
        self.assertFalse(self.toy_small_pool.has_available_toy(self.toy2))
        self.assertFalse(self.toy_small_pool.has_available_toy(self.toy3))
        self.assertFalse(self.toy_small_pool.has_available_toy(self.toy4))

        self.elf.wait_till_next_day()
        self.toy_small_pool.update_available_toy_list_according_to_elf(self.elf)

        self.assertEquals(self.toy_small_pool.length_waiting_list(), 0)
        self.assertEquals(self.toy_small_pool.length_available_list(), 4)

        self.assertEquals(self.toy_small_pool.get_available_toy_duration(), [2, 60, 600])

        self.assertTrue(self.toy_small_pool.has_available_toy(self.toy1))
        self.assertTrue(self.toy_small_pool.has_available_toy(self.toy2))
        self.assertTrue(self.toy_small_pool.has_available_toy(self.toy3))
        self.assertTrue(self.toy_small_pool.has_available_toy(self.toy4))

        toy_of_duration_1 = self.toy_small_pool.get_toy_by_duration(1)
        self.assertTrue(toy_of_duration_1 is None)
        self.assertEquals(self.toy_small_pool.get_available_toy_duration(), [2, 60, 600])

        toy_of_duration_3 = self.toy_small_pool.get_toy_by_duration(3)
        self.assertEquals(toy_of_duration_3, self.toy3)

        self.assertEquals(self.toy_small_pool.get_available_toy_duration(), [60, 600])

        self.assertEquals(self.toy_small_pool.length_available_list(), 3)

        toy_of_duration_50 = self.toy_small_pool.get_toy_by_duration(50)
        self.assertTrue(toy_of_duration_50 is None)
        self.assertEquals(self.toy_small_pool.get_available_toy_duration(), [60, 600])

        toy_of_duration_60 = self.toy_small_pool.get_toy_by_duration(60)
        self.assertTrue(toy_of_duration_60 is not None)
        self.assertEquals(self.toy_small_pool.get_available_toy_duration(), [60, 600])

        toy_of_duration_65 = self.toy_small_pool.get_toy_by_duration(65)
        self.assertTrue(toy_of_duration_65 is not None)
        self.assertEquals(self.toy_small_pool.get_available_toy_duration(), [600])

        # Jouet trop grand
        toy_of_duration_650 = self.toy_small_pool.get_toy_by_duration(650)
        self.assertTrue(toy_of_duration_650 is not None)
        self.assertEquals(self.toy_small_pool.get_available_toy_duration(), [])

    def test_pop_toy_from_waiting_list(self):
        
        self.assertEquals(self.toy_small_pool.length_waiting_list(), 4)

        toy_timestamp, toy = self.toy_small_pool.pop_toy_from_waiting_list()

        self.assertEquals(toy_timestamp, 8*60)
        self.assertEquals(toy, self.toy1)

        self.assertEquals(self.toy_small_pool.length_waiting_list(), 3)

    def test_empty(self):
        self.assertTrue(self.toy_empty_pool.empty())



if __name__ == '__main__':
    unittest.main()


