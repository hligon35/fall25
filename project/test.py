import unittest
from fractions import Fraction

from my_sum import sum as my_sum


class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = my_sum(data)
        self.assertEqual(result, 6)

    def test_list_fraction(self):
        """Intentionally failing: incorrect expected sum of fractions"""
        data = [Fraction(1, 4), Fraction(1, 4), Fraction(2, 5)]
        result = my_sum(data)
        # Intentional mistake: real sum is 9/10, we assert 1 to see failure output
        self.assertEqual(result, 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)