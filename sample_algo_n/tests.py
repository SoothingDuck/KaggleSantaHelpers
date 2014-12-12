import unittest
from hours import Hours

class HoursTest(unittest.TestCase):

	def setUp(self):
		self.h = Hours()

	def test_sanctionned(self):
		sanctionned, unsanctionned = self.h.get_sanctioned_breakdown(520, 45)

		self.assertEqual(sanctionned, 25)
		self.assertEqual(unsanctionned, 20)

if __name__ == '__main__':
	unittest.main()
