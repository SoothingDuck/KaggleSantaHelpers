import unittest

class ToyPool:

    def __init__(self):


        # Sequence ordonnées (timestamp, nombre d'objet) pour maintenir les compteurs de nombre d'objets
        self.__timestamp_counters = []

        # Hash : avec en clé un timestamp et en valeur une heap ordonnée par durée d'objet
        self.__hash_heap_toys = {}


    def add_file_content(filename, num_object):
        pass

class ToyPoolTest(unittest.TestCase):

    def setUp(self):
        toy_file = os.path.join(os.getcwd(), '..', 'DATA', 'toys_rev2.csv')
        self.toy_empty_pool = ToyPool()
        self.toy_filled_pool = ToyPool()
        self.toy_filled_pool.add_file_content(toy_file, 10)


    def test_len(self):

        self.assertEqual(len(self.pool), 10)


if __name__ == '__main__':
    unittest.main()

