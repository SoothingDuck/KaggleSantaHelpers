# -*- coding: utf-8 -*-

import math
import datetime
import hours as hrs

class Elf:
    """ Each Elf starts with a rating of 1.0 and are available at 09:00 on Jan 1.  """
    def __init__(self, elfid):
        self.id = elfid
        self.rating = 1.0
        self.next_available_time = 540
        self.rating_increase = 1.02
        self.rating_decrease = 0.90
        
        self.hrs = hrs.Hours()

        self.ref_time = datetime.datetime(2014, 1, 1, 0, 0)

    def get_next_available_time(self):
        """Recupere le next_available_time"""
        return self.next_available_time

    def set_productivity(self, productivity):
        """Mets à jour manuellement la productivité"""
        self.rating = productivity

    def get_productivity(self):
        """Récupère la productivité"""
        return self.rating

    def set_next_available_time(self, minute):
        """Mets à jour manuellement le next available time"""
        self.next_available_time = minute

    def num_of_working_minutes_left(self):
        """Récupère le nombre de minutes de travail restantes"""
        raise Exception("TODO")

    def wait_till_next_day(self):
        """Mets à jour le next available time avec le début de la prochaine journée"""
        num_day = self.next_available_time / 1440
        self.next_available_time = ((num_day+1)*1440) + 540
        

    def __str__(self):
        return "Elf %s : Productivity %f, Next Available : %s" % (self.id, self.rating, self.get_next_available_time())

    def make_toy(self, toy, wcsv):
        """Fait un jouet"""

        # Mise à jour next available time
        start_minute = self.get_next_available_time()
        toy_duration = toy.get_duration()
        toy_required_minutes = int(math.ceil(toy_duration / self.rating))

        sanctioned, unsanctioned = self.hrs.get_sanctioned_breakdown(start_minute, toy_required_minutes)

        # enforce resting time based on the end_minute and the unsanctioned minutes that
        # need to be accounted for.
        end_minute = start_minute + toy_required_minutes
        # print(start_minute, end_minute)
        if unsanctioned == 0:
            if self.hrs.is_sanctioned_time(end_minute):
                self.next_available_time = end_minute
            else:
                self.next_available_time = self.hrs.next_sanctioned_minute(end_minute)
        else:
            self.next_available_time = self.hrs.apply_resting_period(end_minute, unsanctioned)

        # Mise à jour productivité
        self.rating = max(0.25,
                          min(4.0, self.rating * (self.rating_increase ** (sanctioned/60.0)) *
                              (self.rating_decrease ** (unsanctioned/60.0))))

        # Ecriture du jouet
        # print(toy)
        tt = self.ref_time + datetime.timedelta(minutes=start_minute)
        # print "tt : %s" % tt
        time_string = " ".join([str(tt.year), str(tt.month), str(tt.day), str(tt.hour), str(tt.minute)])
        wcsv.writerow([toy.id, self.id, time_string, toy_required_minutes])

        # print(self)
        # print(self.get_next_available_working_time())

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


