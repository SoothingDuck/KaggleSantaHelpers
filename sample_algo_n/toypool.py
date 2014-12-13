import unittest

class ToyPool:

    def __init__(self):
        pass

class ToyPoolTest(unittest.TestCase):

    def setUp(self):
        self.toy_pool = ToyPool(10000)

    def test_len(self):

        self.assertEqual(len(self.pool), 10000)

    def test_get_toy(self):

        toy = self.toy_pool.pop()

    def test_len_for_day(self):

        self.assertEqual(self.pool.len_for_day(datetime.date(2014, 1, 1))


