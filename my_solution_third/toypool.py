# -*- coding: utf-8 -*-

import csv
import heapq
from toy import Toy

class ToyPool:
    """List of Toys to make"""

    def __init__(self):
        pass

    def __len__(self):
        """Retourne la taille du toy pool"""
        return self.__toy_counter

    def add_file_content(self, toy_file, num_toys=None):
        """Ajout de jouets à partir d'un fichier"""
        i = 0
        with open(toy_file, 'rb') as f:
            fcsv = csv.reader(f)
            fcsv.next()  # header row
            for row in fcsv:
                i += 1
                new_toy = Toy(row[0], row[1], row[2])
                self.push_toy(new_toy)

                if self.length_waiting_list() % 1000 == 0:
                    print self.length_waiting_list()

                if num_toys is not None and i >= num_toys:
                    break

        if num_toys is not None and self.length_waiting_list() != num_toys:
            print '\n ** Read a file with {0} toys, expected {1} toys. Exiting.'.format(self.length_waiting_list(), num_toys)
            exit(-1)


