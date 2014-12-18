# -*- coding: utf-8 -*-

import unittest
import datetime
import math
from hours import Hours

class Toy:
    def __init__(self, toyid, arrival, duration):
        self.reference_start_time = datetime.datetime(2014, 1, 1, 0, 0)  # set when elf starts working on toy
        self.id = toyid
        self.arrival_minute = Hours.convert_to_minute(arrival)
        self.duration = int(duration)
        self.completed_minute = 0

        self.__time_base = datetime.datetime(2014, 1, 1, 0, 0)

    def __str__(self):
        return "Toy %s : Arrival %s, Duration %s, Completed %s" % (self.id, self.arrival_minute, self.duration, self.completed_minute)

    def get_toy_duration(self):
        """Renvoi la dur√©e de cr√©ation d'un objet"""
        return self.duration

    def outside_toy_start_period(self, start_minute):
        """ Checks that work on toy does not start outside of the allowed starting period.
        :param hrs: Hours class
        :param start_minute: minute the work is scheduled to start
        :return: True of outside of allowed starting period, False otherwise
        """
        return start_minute < self.arrival_minute

    def is_complete(self, start_minute, elf_duration, rating):
        """ Determines if the toy is completed given duration of work and elf's productivity rating
        :param start_minute: minute work started
        :param elf_duration: duration of work in minutes
        :param rating: elf's productivity rating
        :return: Boolean
        """
        if self.duration / rating <= elf_duration:
            self.completed_minute = start_minute + int(math.ceil(self.duration/rating))
            return True
        else:
            return False

    def get_min_possible_working_start_time(self):
        """Selon l'heure d'arrivÈe, retourne le timestamp minimum de dÈbut de travail"""
        current_date = self.reference_start_time + datetime.timedelta(minutes=self.arrival_minute)
        year = current_date.year
        month = current_date.month
        day = current_date.day
        hour = current_date.hour
        minute = current_date.minute

        if hour < 9:
            return datetime.datetime(year, month, day, 9, 0, 0)
        elif hour >= 19 and minute > 0:
            return datetime.datetime(year, month, day, 9, 0, 0) + datetime.timedelta(days=1)
        else:
            return current_date
        

class ToyTest(unittest.TestCase):

    def setUp(self):
        self.toy1 = Toy(1, "2014 1 1 2 0", 600)
        self.toy2 = Toy(2, "2014 1 1 9 30", 600)
        self.toy3 = Toy(3, "2014 1 1 19 30", 600)
        self.toy4 = Toy(3, "2014 1 1 19 00", 300)

    def test_get_min_possible_working_start_time(self):
        self.assertEqual(self.toy1.get_min_possible_working_start_time(), datetime.datetime(2014, 1, 1, 9, 0))
        self.assertEqual(self.toy2.get_min_possible_working_start_time(), datetime.datetime(2014, 1, 1, 9, 30))
        self.assertEqual(self.toy3.get_min_possible_working_start_time(), datetime.datetime(2014, 1, 2, 9, 0))
        self.assertEqual(self.toy4.get_min_possible_working_start_time(), datetime.datetime(2014, 1, 1, 19, 0))


if __name__ == '__main__':
    unittest.main()

