# -*- coding: utf-8 -*-

import heapq
from elf import Elf

class ElfPool:

    def __init__(self, n):
        # Liste des elfes triés par temps de disponibilité
        self.__heap_elf = []
        for i in range(n):
            heapq.heappush(self.__heap_elf, (540, Elf(i)))

    def __len__(self):
        """Taille du pool"""
        return len(self.__heap_elf)

    def update_elf(self, elf):
        """Mets à jour un elfe dans le pool"""
        heapq.heappush(self.__heap_elf, (elf.get_next_available_time(), elf))

    def next_available_elf(self):
        """Prend le prochain elfe disponible"""
        next_available_time, elf = heapq.heappop(self.__heap_elf)
        return elf



