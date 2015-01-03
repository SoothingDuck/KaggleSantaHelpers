# -*- coding: utf-8 -*-

import csv
import heapq
import bisect
from toy import Toy

class ToyPool:
    """List of Toys to make"""

    def __init__(self):

        # Heap classant les jouets par ordre d'arriv�e
        self.__waiting_timestamp_heap = []

        # Available possible toy duration
        self.__available_toy_duration = []

        # Available toy by duration
        self.__hash_toy_duration_timestamp = {}
        self.__hash_toy_duration_values = {}
        self.__hash_all_toys = {}

        # Available toy counter
        self.__available_toy_count = 0

    def get_available_toy_duration(self):
        """Retourne la liste des durations possibles"""
        return self.__available_toy_duration

    def get_hash_toy_duration_timestamp(self):
        return self.__hash_toy_duration_timestamp

    def get_hash_toy_duration_values(self):
        return self.__hash_toy_duration_values

    def pop_toy_from_waiting_list(self):
        """Prends un jouet de la waiting list"""
        toy_timestamp, toy = heapq.heappop(self.__waiting_timestamp_heap)
        return(toy_timestamp, toy)

    def push_toy_in_available_list(self, toy):
        """Rends le jouet disponible"""
        duration = toy.get_duration()

        # Verifie si l'index existe d�j�
        i = bisect.bisect_left(self.__available_toy_duration, duration)
        if i != len(self.__available_toy_duration) and self.__available_toy_duration[i] == duration:
            # Ok la valeur existe on ne fait rien
            pass
        else:
            # On l'ajoute
            self.__available_toy_duration.insert(i, duration)

        # Update hash all toys
        id = toy.get_id()
        self.__hash_all_toys[id] = 1

        # Update hash duration
        if not self.__hash_toy_duration_timestamp.has_key(duration):
            self.__hash_toy_duration_timestamp[duration] = []
            self.__hash_toy_duration_values[duration] = []

        self.__hash_toy_duration_timestamp[duration].append(toy.get_arrival_minute())
        self.__hash_toy_duration_values[duration].append(toy)

        # Mise � jour du toy count
        self.__available_toy_count += 1

    def get_toy_by_duration_for_elf(self, elf, duration):
        """Recupere par duration"""
        elf_timestamp = elf.get_next_available_time()

        # Indice de la duration la plus proche 100 => [1, 50, 101] => 1
        i = bisect.bisect_right(self.__available_toy_duration, duration)

        # Indice 0, la duration est inf�rieure � la duration la plus petite
        if i == 0:
            return
        
        while True:
            possible_durations = self.__available_toy_duration[:i]
            
            for duration_found in reversed(possible_durations):

                j = bisect.bisect_right(self.__hash_toy_duration_timestamp[duration_found], elf_timestamp)

                if j != 0:
                    break

            if j == 0:
                return None
            
            toy = self.__hash_toy_duration_values[duration_found].pop(j-1)
            toy_timestamp = self.__hash_toy_duration_timestamp[duration_found].pop(j-1)

            toy_id = toy.get_id()


            if self.__hash_all_toys.has_key(toy_id):
                del self.__hash_all_toys[toy_id]
                if self.__hash_toy_duration_timestamp[duration_found] == []:
                    del self.__hash_toy_duration_timestamp[duration_found]
                    del self.__hash_toy_duration_values[duration_found]
                    del self.__available_toy_duration[self.__available_toy_duration.index(duration_found)]
                self.__available_toy_count -= 1
                return toy

    def get_next_longest_toy_for_elf(self, elf):
        """Recupere le jouet le plus court suivant"""

        elf_timestamp = elf.get_next_available_time()

        possible_durations = self.__available_toy_duration

        for i in reversed(xrange(len(possible_durations))):
            duration_found = possible_durations[i]
            min_toy_duration = self.__hash_toy_duration_timestamp[duration_found][0]

            if min_toy_duration <= elf_timestamp:

                toy_timestamp = self.__hash_toy_duration_timestamp[duration_found].pop(0)
                toy = self.__hash_toy_duration_values[duration_found].pop(0)
                toy_id = toy.get_id()
                if self.__hash_all_toys.has_key(toy_id):
                    del self.__hash_all_toys[toy_id]
                    if self.__hash_toy_duration_timestamp[duration_found] == []:
                        del self.__hash_toy_duration_timestamp[duration_found]
                        del self.__hash_toy_duration_values[duration_found]
                        del self.__available_toy_duration[self.__available_toy_duration.index(duration_found)]
                    self.__available_toy_count -= 1
                    return toy

    def get_next_shortest_toy_for_elf(self, elf):
        """Recupere le jouet le plus court suivant"""

        elf_timestamp = elf.get_next_available_time()

        possible_durations = self.__available_toy_duration

        for i in xrange(len(possible_durations)):
            duration_found = possible_durations[i]
            min_toy_duration = self.__hash_toy_duration_timestamp[duration_found][0]

            if min_toy_duration <= elf_timestamp:

                toy_timestamp = self.__hash_toy_duration_timestamp[duration_found].pop(0)
                toy = self.__hash_toy_duration_values[duration_found].pop(0)
                toy_id = toy.get_id()
                if self.__hash_all_toys.has_key(toy_id):
                    del self.__hash_all_toys[toy_id]
                    if self.__hash_toy_duration_timestamp[duration_found] == []:
                        del self.__hash_toy_duration_timestamp[duration_found]
                        del self.__hash_toy_duration_values[duration_found]
                        del self.__available_toy_duration[self.__available_toy_duration.index(duration_found)]
                    self.__available_toy_count -= 1
                    return toy

    def has_available_toy(self, toy):
        """Le jouet est-il disponible"""
        id = toy.get_id()
        return self.__hash_all_toys.has_key(id)

    def update_available_toy_list_according_to_elf(self, elf):
        """Mets � jour la liste des cadeaux disponibles"""
        if self.length_waiting_list() > 0:
            elf_timestamp = elf.get_next_available_time()

            while True:
                if self.length_waiting_list() <= 0:
                    break

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
        """Ajout de jouets � partir d'un fichier"""
        i = 0
        with open(toy_file, 'rb') as f:
            fcsv = csv.reader(f)
            fcsv.next()  # header row
            for row in fcsv:
                i += 1
                new_toy = Toy(row[0], row[1], row[2], "int")
                self.push_toy_in_waiting_list(new_toy)

                if self.length_waiting_list() % 1000 == 0:
                    print self.length_waiting_list()

                if num_toys is not None and i >= num_toys:
                    break

        if num_toys is not None and self.length_waiting_list() != num_toys:
            print '\n ** Read a file with {0} toys, expected {1} toys. Exiting.'.format(self.length_waiting_list(), num_toys)
            exit(-1)


