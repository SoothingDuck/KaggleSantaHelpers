# -*- coding: utf-8 -*-

import unittest
import math
import hours as hrs
import datetime
import os
import csv

from toy import Toy

class Elf:
    """ Each Elf starts with a rating of 1.0 and are available at 09:00 on Jan 1.  """
    def __init__(self, elfid, start_working_time = datetime.datetime(2014,1,1,9,0,0)):
        self.id = elfid
        self.rating = 1.0
        self.next_available_working_time = start_working_time
        self.next_available_time = 540
        self.rating_increase = 1.02
        self.rating_decrease = 0.90
        
        self.hrs = hrs.Hours()

        self.__time_base = datetime.datetime(2014,1,1,0,0,0)

    def __str__(self):
        return "Elf %s : Productivity %f, Next Available : %s" % (self.id, self.rating, self.get_next_available_working_time())


    def tick_to_next_minute(self):
        """Avance à la prochaine minute disponible de l'elfe"""
        available_time = self.get_next_available_working_time()

        if available_time.hour == 18 and available_time.minute == 59:
            self.next_available_working_time = available_time + datetime.timedelta(minutes=9*60+5*60+1)
        else:
            self.next_available_working_time = available_time + datetime.timedelta(minutes=1)

    def make_toy(self, toy, wcsv):
        """Fait un jouet"""

        # Mise à jour next available time
        current_available_working_time = self.get_next_available_working_time()
        start_minute = int(((current_available_working_time-self.__time_base).seconds)/60)
        toy_duration = toy.get_duration()
        toy_required_minutes = int(math.ceil(toy_duration / self.rating))

        sanctioned, unsanctioned = self.hrs.get_sanctioned_breakdown(start_minute, toy_required_minutes)

        # enforce resting time based on the end_minute and the unsanctioned minutes that
        # need to be accounted for.
        end_minute = start_minute + toy_required_minutes
        # print(start_minute, end_minute)
        if unsanctioned == 0:
            if self.hrs.is_sanctioned_time(end_minute):
                #self.next_available_time = end_minute
                self.set_next_available_working_time(current_available_working_time+datetime.timedelta(minutes=end_minute-start_minute))
            else:
                #self.next_available_time = self.hrs.next_sanctioned_minute(end_minute)
                self.set_next_available_working_time(current_available_working_time+datetime.timedelta(minutes=self.hrs.next_sanctioned_minute(end_minute)-start_minute))
        else:
            #self.next_available_time = self.hrs.apply_resting_period(end_minute, unsanctioned)
            self.set_next_available_working_time(current_available_working_time+datetime.timedelta(minutes=self.hrs.apply_resting_period(end_minute, unsanctioned)-start_minute))

        # Mise à jour productivité
        self.rating = max(0.25,
                          min(4.0, self.rating * (self.rating_increase ** (sanctioned/60.0)) *
                              (self.rating_decrease ** (unsanctioned/60.0))))

        # Ecriture du jouet
        # print(toy)
        tt = datetime.datetime(2014, 1, 1, 0, 0) + datetime.timedelta(seconds=60*start_minute)
        # print "tt : %s" % tt
        time_string = " ".join([str(tt.year), str(tt.month), str(tt.day), str(tt.hour), str(tt.minute)])
        wcsv.writerow([toy.id, self.id, time_string, toy_required_minutes])

        # print(self)
        # print(self.get_next_available_working_time())

    def set_rating(self, rating):
        """Met à jour manuellement le rating de l'elfe"""
        self.rating = rating

    def apply_strategy_for(self, thetoypool, theelfpool, wcsv):
        """Procedure la plus complexe, applique la stratégie de l'elfe selectionné pour un toypool et un elfpool donné"""
        # Si rien on sort
        if len(thetoypool) == 0:
            return

        # print(self)
        # Recupération d'un jouet au hasard dans le toy pool que l'elfe pourrai faire
        toy = thetoypool.get_random_toy_for_elf(self)
        # print(len(thetoypool), len(theelfpool))
        # print(toy)

        # Cas 1 : L'elfe dispose d'assez de temps pour réaliser le jouet dans la journée
        if(self.will_finish_toy_in_sanctionned_hours(toy)):
            self.make_toy(toy, wcsv)
        else:
        # Cas 2 : L'elfe ne dispose d'assez de temps pour réaliser le jouet dans la journée
            while True:
                short_toy = thetoypool.get_next_short_toy_for(self)

                if self.will_finish_toy_in_sanctionned_hours(short_toy):
                    self.make_toy(short_toy, wcsv)
                else:
                    self.make_toy(short_toy, wcsv)
                    self.make_toy(toy, wcsv)
                    break

    def set_next_available_working_time(self, thetimestamp):
        """Mets à jour manuellement le working time"""
        self.next_available_working_time = thetimestamp
        self.next_available_time = int(((thetimestamp-self.__time_base).seconds)/60)

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

        soln_file = os.path.join(os.getcwd(), 'test.csv')
        self.wcsv = csv.writer(open(soln_file, "wb"))


    def test_get_available_time(self):
        elf = Elf(1)
        self.assertEqual(elf.get_next_available_working_time(), datetime.datetime(2014,1,1,9,0,0))
        elf.set_next_available_working_time(datetime.datetime(2014, 1, 1, 11, 40))
        self.assertEqual(elf.get_next_available_working_time(), datetime.datetime(2014,1,1,11,40,0))


    def test_make_toy(self):
        elf1 = Elf(1, datetime.datetime(2014, 1, 1, 9, 0, 0))
        elf2 = Elf(2, datetime.datetime(2014, 1, 1, 9, 0, 0))
        elf3 = Elf(3, datetime.datetime(2014, 1, 1, 18, 59, 0))

        elf2.set_rating(2)

        toy1 = Toy(1, "2014 1 1 0 0", 600)
        toy2 = Toy(2, "2014 1 1 0 0", 600)
        toy3 = Toy(3, "2014 1 1 0 0", 1)
        toy4 = Toy(4, "2014 1 1 0 0", 2)

        elf1.make_toy(toy1, self.wcsv)
        self.assertEquals(elf1.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 9, 0, 0))

        elf1.make_toy(toy3, self.wcsv)
        self.assertEquals(elf1.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 9, 1, 0))

        elf2.make_toy(toy2, self.wcsv)
        self.assertEquals(elf2.get_next_available_working_time(), datetime.datetime(2014, 1, 1, 14, 0, 0))

        elf3.make_toy(toy4, self.wcsv)
        self.assertEquals(elf3.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 9, 1, 0))

    def test_will_finish_toy_in_sanctionned_hours(self):
        toy1 = Toy(1, "2014 1 1 0 0", 600)
        toy2 = Toy(1, "2014 1 1 0 0", 601)

        self.assertTrue(self.elf_productivity_1.will_finish_toy_in_sanctionned_hours(toy1))
        self.assertFalse(self.elf_productivity_1.will_finish_toy_in_sanctionned_hours(toy2))

        self.assertTrue(self.elf_productivity_2.will_finish_toy_in_sanctionned_hours(toy1))
        self.assertTrue(self.elf_productivity_2.will_finish_toy_in_sanctionned_hours(toy2))

    def test_tick_to_next_minute(self):

        elf = Elf(1, datetime.datetime(2014, 1, 1, 18, 58, 0))

        self.assertEquals(elf.get_next_available_working_time(), datetime.datetime(2014, 1, 1, 18, 58))

        elf.tick_to_next_minute()
        self.assertEquals(elf.get_next_available_working_time(), datetime.datetime(2014, 1, 1, 18, 59))

        elf.tick_to_next_minute()
        self.assertEquals(elf.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 9, 0))

        elf.tick_to_next_minute()
        self.assertEquals(elf.get_next_available_working_time(), datetime.datetime(2014, 1, 2, 9, 1))

if __name__ == '__main__':
    unittest.main()
