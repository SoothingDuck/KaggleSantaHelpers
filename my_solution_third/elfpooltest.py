# -*- coding: utf-8 -*-

import unittest
from elfpool import ElfPool
from elf import Elf

class ElfPoolTest(unittest.TestCase):

    def setUp(self):
        self.pool = ElfPool(2)


    def test_length(self):
        """Teste la taille du pool"""
        # Taille initiale 2
        self.assertEquals(len(self.pool), 2)

        # Ajout d'un elfe -> taille 3
        self.pool.update_elf(Elf(3))
        self.assertEquals(len(self.pool), 3)


    def test_next_available_elf(self):
        
        elf1 = self.pool.next_available_elf()

        elf1.wait_till_next_day()

        self.pool.update_elf(elf1)

        elf2 = self.pool.next_available_elf()

        self.assertNotEquals(elf1, elf2)

        self.assertTrue(elf2.get_next_available_time() < elf1.get_next_available_time())


if __name__ == '__main__':
    unittest.main()
