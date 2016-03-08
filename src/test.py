import unittest
import calc_rating_of_each_strategy
from calc_rating_of_each_strategy import Result


class TestMain(unittest.TestCase):
    def test_calc_diff_rate0(self):
        expected = 16.0
        actual = calc_rating_of_each_strategy.calc_diff_rate(900, 900, Result.win)
        self.assertEqual(actual, expected)

    def test_calc_diff_rate1(self):
        expected = 24.0
        actual = calc_rating_of_each_strategy.calc_diff_rate(900, 1100, Result.win)
        self.assertEqual(actual, expected)

    def test_calc_diff_rate2(self):
        expected = 8.0
        actual = calc_rating_of_each_strategy.calc_diff_rate(900, 700, Result.win)
        self.assertEqual(actual, expected)

    def test_calc_diff_rate3(self):
        expected = -8.0
        actual = calc_rating_of_each_strategy.calc_diff_rate(900, 1100, Result.lose)
        self.assertEqual(actual, expected)

    def test_calc_diff_rate4(self):
        expected = -16.0
        actual = calc_rating_of_each_strategy.calc_diff_rate(900, 900, Result.lose)
        self.assertEqual(actual, expected)

    def test_calc_diff_rate5(self):
        expected = 1.0
        actual = calc_rating_of_each_strategy.calc_diff_rate(900, 0, Result.win)
        self.assertEqual(actual, expected)

    def test_calc_diff_rate5(self):
        expected = 31.0
        actual = calc_rating_of_each_strategy.calc_diff_rate(900, 1300, Result.win)
        self.assertEqual(actual, expected)




if __name__ == '__main__':
    unittest.main()
