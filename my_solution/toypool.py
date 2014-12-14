import unittest

class ToyPool:

    def __init__(self):
        # ordonné par ordre d'arrivée
        self.__all_toys = []

        # hash : key durée, value tableau ordonné par date de disponibilité


    def 

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

