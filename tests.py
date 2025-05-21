import unittest
from random import randint

from script import *
from run import Shell, _parse_num


class NumberBreakerTests(unittest.TestCase):
    # num testing
    def test_float(self):
        self.assertRaises(ValueError, break_down, num=123.123, power_step=3)

    def test_type_list(self):
        self.assertRaises(TypeError, break_down, num=[123], power_step=3)

    def test_type_float(self):
        self.assertEqual({0: 123}, break_down(num=123.000, power_step=3))

    def test_empty(self):
        self.assertRaises(TypeError, break_down, num=None, power_step=3)

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
    def test_float_power_step(self):
        self.assertRaises(TypeError, break_down, num=123, power_step=3.1)

    def test_list_power_step(self):
        self.assertRaises(TypeError, break_down, num=123, power_step=[3.1])

    def test_negative_power_step(self):
        self.assertRaises(ValueError, break_down, num=123, power_step=-3)

    def test_zero_power_step(self):
        self.assertRaises(ValueError, break_down, num=123, power_step=0)

    def test_string_power_step(self):
        self.assertRaises(TypeError, break_down, num=123, power_step="3")

    def test_random_power_step(self):
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


class BatchTests(unittest.TestCase):
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


class AssemblerTests(unittest.TestCase):
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


class CurrencySpellerTests(unittest.TestCase):
    def test_string_type(self):
        self.assertRaises(TypeError, currency_speller, num="123456", power_names=POWER_NAMES, num_names=NUM_NAMES)

    def test_list_type(self):
        self.assertRaises(TypeError, currency_speller, num=[123456], power_names=POWER_NAMES, num_names=NUM_NAMES)

    def test_predefined_int(self):
        predefined_inputs = {
            0: "",
            -1: "Minus one dollar",
            14: "Fourteen dollars",
            -12: "Minus twelve dollars",
            345_001_000: "Three hundred forty-five million one thousand dollars",
            1_000_001: "One million one dollars",
            901_001_437_010: "Nine hundred one billion one million four hundred thirty-seven thousand ten dollars",
            -123_123: "Minus one hundred twenty-three thousand one hundred twenty-three dollars",
            12_000_013: "Twelve million thirteen dollars",
        }
        for num, expected in predefined_inputs.items():
            self.assertEqual(expected, currency_speller(num, power_names=POWER_NAMES, num_names=NUM_NAMES))

    def test_predefined_float(self):
        predefined_inputs = {
            456_234.00001: "Four hundred fifty-six thousand two hundred thirty-four dollars",
            123.123: "One hundred twenty-three dollars and twelve cents",
            -123.0: "Minus one hundred twenty-three dollars",
            123.1: "One hundred twenty-three dollars and ten cents",
            -123.4: "Minus one hundred twenty-three dollars and forty cents",
            123.1000: "One hundred twenty-three dollars and ten cents",
            123.14: "One hundred twenty-three dollars and fourteen cents",
            123.01: "One hundred twenty-three dollars and one cent",
            123.1001: "One hundred twenty-three dollars and ten cents",
        }
        for num, expected in predefined_inputs.items():
            self.assertEqual(expected, currency_speller(num, power_names=POWER_NAMES, num_names=NUM_NAMES))


class ApplicationParserTests(unittest.TestCase):
    shell = Shell()

    def test_underscores(self):
        expected = 1234
        got = _parse_num("1_2_3_4$")
        self.assertEqual(expected, got)

    def test_leading_0s(self):
        expected = 1234
        got = _parse_num("0001234$")
        self.assertEqual(expected, got)

    def test_bad_input(self):
        bad_inputs = [
            "a123b$",
            "abc$",
            "1-1235-123&$",
            "-bscb$",
            "1e5.120$",
            "$Minus two",
            "550$/",
            "5501",
            "$\34522350",
            r"\34522350$",
            "/12345$",
            "-"
        ]

        for inp in bad_inputs:
            self.assertRaises(ValueError, _parse_num, inp)

    def test_splitter(self):
        inputs = {
            123: (123, 0.0),
            123.123: (123, 0.123),
            -123: (-123, 0.0),
            -123.123: (-123, -0.123),
            0.12: (0.0, 0.12),
            -0.95: (0.0, -0.95)
        }

        for inp, exp in inputs.items():
            self.assertEqual(exp, split_decimal(inp))


if __name__ == '__main__':
    unittest.main()
