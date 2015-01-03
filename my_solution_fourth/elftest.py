# -*- coding: utf-8 -*-

import unittest

from elf import Elf

class ElfTest(unittest.TestCase):

    def setUp(self):
        self.elf1 = Elf(1)
        self.elf2 = Elf(2)

        # soln_file = os.path.join(os.getcwd(), 'test.csv')
        # self.wcsv = csv.writer(open(soln_file, "wb"))

    def test_num_of_working_minutes_left(self):

        self.assertEquals(self.elf1.num_of_working_minutes_left(), 600)

        self.elf1.set_next_available_time(600)

        self.assertEquals(self.elf1.num_of_working_minutes_left(), 600-60)

        self.elf1.set_next_available_time(540 + 595)

        self.assertEquals(self.elf1.num_of_working_minutes_left(), 5)

        self.elf1.set_next_available_time(540 + 605)

        self.assertEquals(self.elf1.num_of_working_minutes_left(), 0)

    def test_get_productivity(self):

        self.assertEquals(self.elf1.get_productivity(), 1.0)

        self.elf1.set_productivity(2.0)

        self.assertEquals(self.elf1.get_productivity(), 2.0)

    def test_wait_till_next_day(self):

        self.assertEquals(self.elf1.get_next_available_time(), 540)

        self.elf1.set_next_available_time(700)

        self.assertEquals(self.elf1.get_next_available_time(), 700)

        self.elf1.wait_till_next_day()

        self.assertEquals(self.elf1.get_next_available_time(), 1440+(9*60))

        self.elf1.wait_till_next_day()

        self.assertEquals(self.elf1.get_next_available_time(), (2*1440)+(9*60))
        
if __name__ == '__main__':
    unittest.main()
