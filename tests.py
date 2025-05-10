import unittest
from random import randint
from main import *


class FunctionTests(unittest.TestCase):
    # support func testing
    def test_batched_backwards(self):
        iterables = {
            "hello world": [tuple("rld"), tuple(" wo"), tuple("llo"), tuple("he")],
            (1, 2, 3, 4, 5, 6, 7): [(5, 6, 7), (2, 3, 4), (1,)]
        }
        n = 3
        for inp, expected in iterables.items():
            got = list(batched(inp, n, backwards=True))
            self.assertListEqual(expected, got)

    def test_batched(self):
        iterables = {
            "hello world": [tuple("hel"), tuple("lo "), tuple("wor"), tuple("ld")],
            (1, 2, 3, 4, 5, 6, 7): [(1, 2, 3), (4, 5, 6), (7,)]
        }
        n = 3
        for inp, expected in iterables.items():
            got = list(batched(inp, n, backwards=False))
            self.assertListEqual(expected, got)

    def test_batched_edge(self):
        iterables = {
            # "h": ("h",),
            tuple(): []
        }
        n = 3
        for inp, expected in iterables.items():
            got = list(batched(inp, n, backwards=False))
            self.assertListEqual(expected, got)

    # testing assembler
    def test_assembler_edge(self):
        iterables = [
            [{0: 0}, 0],
            [{6: 123, 3: 456, 0: 789}, 123_456_789],
            [{0: 123}, 123],
            [{2: 4, 1: 3, 0: 1}, 431],
            [{3: 5, 0: 1}, 5001],
        ]

        for inp, expected in iterables:
            got = assemble(inp)
            self.assertEqual(expected, got)

    def test_assembler_random(self):
        for i in range(10_000):
            num = randint(0, 10 ** 27)
            step = randint(1, 20)
            broken_num = break_down(num, power_step=step)
            got = assemble(broken_num)
            self.assertEqual(num, got)

    def test_bad_assembler_input(self):
        self.assertRaises(ValueError, assemble, {})
        self.assertRaises(TypeError, assemble, "hello")

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
        self.assertRaises(ValueError, break_down, num=123.123, power_step=3)

    def test_type_float(self):
        self.assertEqual({0: 123}, break_down(num=123.000, power_step=3))

    def test_empty(self):
        self.assertEqual({0: 0}, break_down(num=0, power_step=3))

    def test_negative(self):
        self.assertRaises(ValueError, break_down, num=-123, power_step=3)

    def test_zero(self):
        self.assertEqual({0: 0}, break_down(num=0, power_step=3))

    def test_string(self):
        self.assertRaises(TypeError, break_down, num="123456", power_step=3)

    def test_random_num(self):
        for i in range(10_000):
            expected = randint(0, 10 ** 27)
            result = break_down(num=expected, power_step=3)

            got = 0
            for power, value in result.items():
                got += (10 ** power) * value

            self.assertEqual(expected, got)

    # power_step testing
    def test_float_denominator(self):
        self.assertRaises(TypeError, break_down, num=123, power_step=3.1)

    def test_negative_denominator(self):
        self.assertRaises(ValueError, break_down, num=123, power_step=-3)

    def test_zero_denominator(self):
        self.assertRaises(ValueError, break_down, num=123, power_step=0)

    def test_string_denominator(self):
        self.assertRaises(TypeError, break_down, num=123, power_step="3")

    def test_random_denominator(self):
        for i in range(10_000):
            denominator = randint(1, 20)
            result = break_down(num=123_456_789, power_step=denominator)

            got = 0
            for power, value in result.items():
                got += (10 ** power) * value

            self.assertEqual(123_456_789, got)

    # testing both at the same time
    def test_random_num_denom(self):
        for i in range(100_000):
            power_step = randint(1, 20)
            num = randint(1, 10 ** 27)
            result = break_down(num=num, power_step=power_step)

            got = 0
            for power, value in result.items():
                got += (10 ** power) * value

            self.assertEqual(num, got)


if __name__ == '__main__':
    unittest.main()
