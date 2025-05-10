import unittest
from random import randint
from main import *


class Tests(unittest.TestCase):
    # support func testing
    def test_batched_backwards(self):
        iterable = "hello world"
        n = 3

        expected = [tuple("rld"), tuple(" wo"), tuple("llo"), tuple("he")]
        got = list(batched_backwards(iterable, n))
        self.assertEqual(expected, got)

    # number speller edge cases
    def test_speller_float_type(self):
        self.assertRaises(TypeError, number_speller, num=123.123, power_names=POWER_NAMES, num_names=NUM_NAMES)

    def test_speller_string_type(self):
        self.assertRaises(TypeError, number_speller, num="123456", power_names=POWER_NAMES, num_names=NUM_NAMES)

    def test_speller_predefined(self):
        predefined_inputs = {
            0: "",
            -1: "Minus one",
            14: "Fourteen",
            345_001_000: "Three hundred forty five million one thousand",
            1_000_001: "One million one",
            901_001_437_010: "Nine hundred one billion one million four hundred thirty seven thousand ten",
            -123_123: "Minus one hundred twenty three thousand one hundred twenty three"
        }
        for num, expected in predefined_inputs.items():
            self.assertEqual(expected, number_speller(num, power_names=POWER_NAMES, num_names=NUM_NAMES))

    # 1_234_567_8910 -> ignore _
    # 1,234,234,345.50 -> treat as integer
    # 1.235.3456.236 -> treat as integer
    # 0000.0000.123235 -> ignore leading 0 and _

    # number break down testing
    # num testing
    def test_float(self):
        self.assertRaises(ValueError, break_down, num=123.123, denominator=3)

    def test_type_float(self):
        self.assertEqual({0: 123}, break_down(num=123.000, denominator=3))

    def test_empty(self):
        self.assertEqual({0: 0}, break_down(num=0, denominator=3))

    def test_negative(self):
        self.assertRaises(ValueError, break_down, num=-123, denominator=3)

    def test_zero(self):
        self.assertEqual({0: 0}, break_down(num=0, denominator=3))

    def test_string(self):
        self.assertRaises(TypeError, break_down, num="123456", denominator=3)

    def test_random_num(self):
        for i in range(10_000):
            expected = randint(0, 10 ** 27)
            result = break_down(num=expected, denominator=3)

            got = 0
            for power, value in result.items():
                got += (10 ** power) * value

            self.assertEqual(expected, got)

    # denominator testing
    def test_float_denominator(self):
        self.assertRaises(TypeError, break_down, num=123, denominator=3.1)

    def test_negative_denominator(self):
        self.assertRaises(ValueError, break_down, num=123, denominator=-3)

    def test_zero_denominator(self):
        self.assertRaises(ValueError, break_down, num=123, denominator=0)

    def test_string_denominator(self):
        self.assertRaises(TypeError, break_down, num=123, denominator="3")

    def test_random_denominator(self):
        for i in range(10_000):
            denominator = randint(1, 20)
            result = break_down(num=123_456_789, denominator=denominator)

            got = 0
            for power, value in result.items():
                got += (10 ** power) * value

            self.assertEqual(123_456_789, got)

    # testing both at the same time
    def test_random_num_denom(self):
        for i in range(100_000):
            denominator = randint(1, 20)
            num = randint(1, 10 ** 27)
            result = break_down(num=num, denominator=denominator)
a
            got = 0
            for power, value in result.items():
                got += (10 ** power) * value

            self.assertEqual(num, got)


if __name__ == '__main__':
    unittest.main()
