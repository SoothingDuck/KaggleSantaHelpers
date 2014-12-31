# -*- coding: utf-8 -*-

import unittest
import os

from toypool import ToyPool
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
        self.toy_small_pool.push_toy_in_waiting_list(self.toy1)
        self.toy_small_pool.push_toy_in_waiting_list(self.toy2)
        self.toy_small_pool.push_toy_in_waiting_list(self.toy3)

    def test_pop_toy_from_waiting_list(self):
        
        self.assertEquals(self.toy_small_pool.length_waiting_list(), 3)

        toy_timestamp, toy = self.toy_small_pool.pop_toy_from_waiting_list()

        self.assertEquals(toy_timestamp, 8*60)
        self.assertEquals(toy, self.toy1)

    def test_empty(self):
        self.assertTrue(self.toy_empty_pool.empty())



if __name__ == '__main__':
    unittest.main()


