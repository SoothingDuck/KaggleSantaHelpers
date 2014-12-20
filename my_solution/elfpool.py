import unittest

class ElfPool:

    def __init__(self, n):
        pass

class ElfPoolTest(unittest.TestCase):

    def setUp(self):
        self.pool = ElfPool()
        self.pool.add_elf(1, datetime.datetime(2014, 1, 2, 9, 0, 0))


    def test_empty_for_working_date(self):
        # Y-a-t-il des elfes ou non disponibles avant cette date
        self.assertTrue()

if __name__ == '__main__':
    unittest.main()
