# -*- coding: utf-8 -*-

import unittest
import math
import hours as hrs
import datetime
from toy import Toy

class Elf:
    """ Each Elf starts with a rating of 1.0 and are available at 09:00 on Jan 1.  """
    def __init__(self, elfid):
        self.id = elfid
        self.rating = 1.0
        self.next_available_time = 540  # Santa's Workshop opens Jan 1, 2014 9:00 (= 540 minutes)
        self.rating_increase = 1.02
        self.rating_decrease = 0.90

        self.__time_base = datetime.datetime(2014,1,1,0,0,0)

    def set_next_available_time(self, next_timestamp):
        """Deplace le next available time"""
        current_available_time =  self.__time_base + datetime.timedelta(minutes=self.next_available_time)
        minutes_diff = int(((next_timestamp-current_available_time)/60).total_seconds())
        self.next_available_time = self.next_available_time + minutes_diff

    def will_finish_toy_in_sanctionned_hours(self, toy):
        """Retourne True si l'heure de fin de création du jouet est entre 9h et 19h"""
        if toy.get_duration() > 600:
            return False

        toy_finish_timestamp = self.get_available_time() + datetime.timedelta(minutes=toy.get_duration())

        if toy_finish_timestamp.hour > 19 or (toy_finish_timestamp.hour == 19 and toy_finish_timestamp.minute > 0):
            return False

        if toy_finish_timestamp.hour < 9:
            return False

        return True
        

    def get_available_time_in_minutes(self):
        """Retourne le next available time"""
        return self.next_available_time

    def __str__(self):
        return "Elf %s : Productivity %f, Next Available : %s" % (self.id, self.rating, self.next_available_time)

    def get_available_time(self):
        return self.__time_base + datetime.timedelta(minutes=self.next_available_time)

    def will_finish_toy_in_sanctionned_hours(self, toy):
        pass

    def update_elf(self, hrs, toy, start_minute, duration):
        """ Updates the elf's productivity rating and next available time based on last toy completed.
        :param hrs: Hours object for bookkeeping
        :param toy: Toy object for the toy the elf just finished
        :param start_minute: minute work started
        :param duration: duration of work, in minutes
        :return: void
        """
        self.update_next_available_minute(hrs, start_minute, duration)
        self.update_productivity(hrs, start_minute, int(math.ceil(toy.duration / self.rating)))

    def update_next_available_minute(self, hrs, start_minute, duration):
        """ Apply the resting time constraint and determine the next minute when the elf can work next.
        Here, elf can only start work during sanctioned times
        :param start_minute: time work started on last toy
        :param duration: duration of work on last toy
        :return: void
        """
        sanctioned, unsanctioned = hrs.get_sanctioned_breakdown(start_minute, duration)

        # enforce resting time based on the end_minute and the unsanctioned minutes that
        # need to be accounted for.
        end_minute = start_minute + duration
        if unsanctioned == 0:
            if hrs.is_sanctioned_time(end_minute):
                self.next_available_time = end_minute
            else:
                self.next_available_time = hrs.next_sanctioned_minute(end_minute)
        else:
            self.next_available_time = hrs.apply_resting_period(end_minute, unsanctioned)

    def update_productivity(self, hrs, start_minute, toy_required_minutes):
        """ Update the elf's productivity rating based on the number of minutes the toy required that were
        worked during sanctioned and unsanctioned times.
        max(0.5,
            min(2.0, previous_rating * (self.rating_increase ** sanctioned_hours) *
            (self.rating_decrease ** unsanctioned_hours)))
        :param hrs: hours object
        :param start_minute: minute work started
        :param toy_required_minutes: minutes required to build the toy (may be different from minutes elf worked)
        :return: void
        """
        # number of required minutes to build toy worked by elf, broken up by sanctioned and unsanctioned minutes
        sanctioned, unsanctioned = hrs.get_sanctioned_breakdown(start_minute, toy_required_minutes)
        self.rating = max(0.25,
                          min(4.0, self.rating * (self.rating_increase ** (sanctioned/60.0)) *
                              (self.rating_decrease ** (unsanctioned/60.0))))


class ElfTest(unittest.TestCase):

    def setUp(self):
        self.elf_productivity_1 = Elf(1)
        self.elf_productivity_2 = Elf(2)
        self.elf_productivity_2.rating = 2


    def test_get_available_time(self):
        elf = Elf(1)
        self.assertEqual(elf.get_available_time(), datetime.datetime(2014,1,1,9,0,0))
        elf.set_next_available_time(datetime.datetime(2014, 1, 1, 11, 40))
        self.assertEqual(elf.get_available_time(), datetime.datetime(2014,1,1,11,40,0))

    def test_will_finish_toy_in_sanctionned_hours(self):
        toy1 = Toy(1, "2014 1 1 0 0", 600)
        toy2 = Toy(1, "2014 1 1 0 0", 601)

        self.assertTrue(self.elf_productivity_1.will_finish_toy_in_sanctionned_hours(toy1))
        self.assertFalse(self.elf_productivity_1.will_finish_toy_in_sanctionned_hours(toy2))

        self.assertTrue(self.elf_productivity_1.will_finish_toy_in_sanctionned_hours(toy1))
        self.assertTrue(self.elf_productivity_2.will_finish_toy_in_sanctionned_hours(toy2))

if __name__ == '__main__':
    unittest.main()
