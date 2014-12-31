# -*- coding: utf-8 -*-

import csv
import heapq
import bisect
from toy import Toy

class ToyPool:
    """List of Toys to make"""

    def __init__(self):

        # Heap classant les jouets par ordre d'arrivée
        self.__waiting_timestamp_heap = []

        # Available possible toy duration
        self.__available_toy_duration = []

        # Available toy by duration
        self.__hash_toy_duration = {}

        # Available toy counter
        self.__available_toy_count = 0


    def pop_toy_from_waiting_list(self):
        """Prends un jouet de la waiting list"""
        toy_timestamp, toy = heapq.heappop(self.__waiting_timestamp_heap)
        return(toy_timestamp, toy)

    def push_toy_in_available_list(self, toy):
        """Rends le jouet disponible"""
        raise Exception("TODO")

    def update_available_toy_list_according_to_elf(self, elf):
        """Mets à jour la liste des cadeaux disponibles"""
        if self.length_waiting_list() > 0:
            elf_timestamp = elf.get_next_available_time()

            while True:
                toy_timestamp, toy = self.pop_toy_from_waiting_list()
                if toy_timestamp <= elf_timestamp:
                    self.push_toy_in_available_list(toy)
                else:
                    self.push_toy_in_waiting_list(toy)
                    break


    def empty(self):
        return (self.length_waiting_list() == 0 and self.__available_toy_count == 0)

    def length_available_list(self):
        """Nombre de jouets disponibles"""
        return self.__available_toy_count

    def length_waiting_list(self):
        """Taille de la file d'attente"""
        return len(self.__waiting_timestamp_heap)

    def push_toy_in_waiting_list(self, toy):
        """Ajoute un jouet dans le pool"""
        heapq.heappush(self.__waiting_timestamp_heap, (toy.get_arrival_minute(), toy))

    def add_file_content(self, toy_file, num_toys=None):
        """Ajout de jouets à partir d'un fichier"""
        i = 0
        with open(toy_file, 'rb') as f:
            fcsv = csv.reader(f)
            fcsv.next()  # header row
            for row in fcsv:
                i += 1
                new_toy = Toy(row[0], row[1], row[2])
                self.push_toy_in_waiting_list(new_toy)

                if self.length_waiting_list() % 1000 == 0:
                    print self.length_waiting_list()

                if num_toys is not None and i >= num_toys:
                    break

        if num_toys is not None and self.length_waiting_list() != num_toys:
            print '\n ** Read a file with {0} toys, expected {1} toys. Exiting.'.format(self.length_waiting_list(), num_toys)
            exit(-1)


