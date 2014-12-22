# -*- coding: utf-8 -*-

import unittest
import math
import hours as hrs
import datetime
from toy import Toy

class Elf:
    """ Each Elf starts with a rating of 1.0 and are available at 09:00 on Jan 1.  """
    def __init__(self, elfid, start_working_time = datetime.datetime(2014,1,1,9,0,0)):
        self.id = elfid
        self.rating = 1.0
        self.next_available_working_time = start_working_time
        self.rating_increase = 1.02
        self.rating_decrease = 0.90

        self.__time_base = datetime.datetime(2014,1,1,0,0,0)

    def __str__(self):
        return "Elf %s : Productivity %f, Next Available : %s" % (self.id, self.rating, self.get_next_available_working_time())


    def set_rating(self, rating):
        """Met à jour manuellement le rating de l'elfe"""
        self.rating = rating

    def apply_strategy_for(self, thetoypool, theelfpool):
        """Procedure la plus complexe, applique la stratégie de l'elfe selectionné pour un toypool et un elfpool donné"""
        print(self)
        # Recupération d'un jouet au hasard dans le toy pool que l'elfe pourrai faire
        toy = thetoypool.get_random_toy_for_elf(self)
        print(len(thetoypool), len(theelfpool))
        print(toy)

        # Cas 1 : L'elfe dispose d'assez de temps pour réaliser le jouet dans la journée
        if(self.will_finish_toy_in_sanctionned_hours(toy)):
            self.make_toy(toy)
        else:
        # Cas 2 : L'elfe ne dispose d'assez de temps pour réaliser le jouet dans la journée
            while True:
                short_toy = thetoypool.get_next_short_toy_for(elf)
                if self.will_finish_toy_in_sanctionned_hours(short_toy):
                    self.make_toy(short_toy)
                else:
                    self.make_toy(short_toy)
                    self.wait_till_next_day()
                    self.make_toy(toy)
                    break

        # On remet l'elfe dans le pool avec sa nouvelle date de disponibilité
        theelfpool.add_elf(self)

    def set_next_available_working_time(self, thetimestamp):
        """Mets à jour manuellement le working time"""
        self.next_available_working_time = thetimestamp

    def get_next_available_working_time(self):
        """Recupere le prochain timestamp de disponibilite de l'elfe"""
        return self.next_available_working_time

    def will_finish_toy_in_sanctionned_hours(self, toy):
        """Le jouet va-t-il être fini dans les heures ouvrées"""
        elf_working_timestamp = self.get_next_available_working_time()
        
        toy_duration = toy.get_duration()

        toy_required_minutes = int(math.ceil(toy_duration / self.rating))

        if toy_required_minutes > 600:
            return False
        else:
            next_elf_working_timestamp = elf_working_timestamp + datetime.timedelta(minutes=toy_required_minutes)
            if next_elf_working_timestamp.date() > elf_working_timestamp.date():
                return False
            else:
                if next_elf_working_timestamp.hour == 19 and next_elf_working_timestamp.minute == 0:
                    return True
                elif next_elf_working_timestamp.hour < 19:
                    return True
                else:
                    return False

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
        self.elf_productivity_3 = Elf(3)
        self.elf_productivity_2.set_rating(2)


    def test_get_available_time(self):
        elf = Elf(1)
        self.assertEqual(elf.get_next_available_working_time(), datetime.datetime(2014,1,1,9,0,0))
        elf.set_next_available_working_time(datetime.datetime(2014, 1, 1, 11, 40))
        self.assertEqual(elf.get_next_available_working_time(), datetime.datetime(2014,1,1,11,40,0))

    def test_make_toy(self):
        elf1 = Elf(1, datetime.datetime(2014, 1, 1, 9, 0, 0))
        elf2 = Elf(2, datetime.datetime(2014, 1, 1, 9, 0, 0))

        elf2.set_rating(2)

        toy1 = Toy(1, "2014 1 1 0 0", 600)
        toy2 = Toy(2, "2014 1 1 0 0", 600)
        toy3 = Toy(3, "2014 1 1 0 0", 1)

        elf1.make_toy(toy1)
        self.assertEquals(elf1.get_next_available_working_time(), datetime.datetime(2014, 1, 1, 19, 0, 0))

        elf1.make_toy(toy3)
        self.assertEquals(elf1.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 9, 1, 0))

        elf2.make_toy(toy2)
        self.assertEquals(elf2.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 14, 0, 0))

    def test_will_finish_toy_in_sanctionned_hours(self):
        toy1 = Toy(1, "2014 1 1 0 0", 600)
        toy2 = Toy(1, "2014 1 1 0 0", 601)

        self.assertTrue(self.elf_productivity_1.will_finish_toy_in_sanctionned_hours(toy1))
        self.assertFalse(self.elf_productivity_1.will_finish_toy_in_sanctionned_hours(toy2))

        self.assertTrue(self.elf_productivity_2.will_finish_toy_in_sanctionned_hours(toy1))
        self.assertTrue(self.elf_productivity_2.will_finish_toy_in_sanctionned_hours(toy2))

if __name__ == '__main__':
    unittest.main()
