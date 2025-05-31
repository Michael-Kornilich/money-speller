import pytest
from random import randint
from scripts.script import *
from scripts.app import POWER_NAMES, NUM_NAMES


class TestNumberBreaker:
    # num testing
    def test_float(self):
        with pytest.raises(ValueError): break_down(num=123.123, power_step=3)

    def test_type_list(self):
        with pytest.raises(TypeError): break_down(num=[123], power_step=3)

    def test_type_float(self):
        assert {0: 123} == break_down(num=123.000, power_step=3)

    def test_empty(self):
        with pytest.raises(TypeError): break_down(num=None, power_step=3)

    def test_negative(self):
        with pytest.raises(ValueError): break_down(num=-123, power_step=3)

    def test_zero(self):
        assert {0: 0} == break_down(num=0, power_step=3)

    def test_string(self):
        with pytest.raises(TypeError): break_down(num="123456", power_step=3)

    def test_random_num(self):
        for i in range(10_000):
            expected = randint(0, 10 ** 27)
            result = break_down(num=expected, power_step=3)

            got = 0
            for power, value in result.items():
                got += (10 ** power) * value

            assert expected == got, f"expected: {expected}. Got: {got}"

    # power_step testing
    def test_float_power_step(self):
        with pytest.raises(TypeError): break_down(num=123, power_step=3.1)

    def test_list_power_step(self):
        with pytest.raises(TypeError): break_down(num=123, power_step=[3.1])

    def test_negative_power_step(self):
        with pytest.raises(TypeError): break_down(num=123, power_step=[3.1])

    def test_zero_power_step(self):
        with pytest.raises(ValueError): break_down(num=123, power_step=0)

    def test_string_power_step(self):
        with pytest.raises(TypeError): break_down(num=123, power_step="3")

    def test_random_power_step(self):
        for i in range(10_000):
            denominator = randint(1, 20)
            result = break_down(num=123_456_789, power_step=denominator)

            got = 0
            for power, value in result.items():
                got += (10 ** power) * value

            assert 123_456_789 == got

    # testing both at the same time
    def test_random_num_denom(self):
        for i in range(100_000):
            power_step = randint(1, 20)
            num = randint(1, 10 ** 27)
            result = break_down(num=num, power_step=power_step)

            got = 0
            for power, value in result.items():
                got += (10 ** power) * value

            assert num == got


class TestBatch:
    def test_batched_backwards(self):
        iterables = {
            "hello world": [tuple("rld"), tuple(" wo"), tuple("llo"), tuple("he")],
            (1, 2, 3, 4, 5, 6, 7): [(5, 6, 7), (2, 3, 4), (1,)]
        }
        n = 3
        for inp, expected in iterables.items():
            got = list(batched(inp, n, backwards=True))
            assert list(expected) == list(got)

    def test_batched(self):
        iterables = {
            "hello world": [tuple("hel"), tuple("lo "), tuple("wor"), tuple("ld")],
            (1, 2, 3, 4, 5, 6, 7): [(1, 2, 3), (4, 5, 6), (7,)]
        }
        n = 3
        for inp, expected in iterables.items():
            got = list(batched(inp, n, backwards=False))
            assert list(expected) == list(got)

    def test_batched_edge(self):
        iterables = {
            # "h": ("h",),
            tuple(): []
        }
        n = 3
        for inp, expected in iterables.items():
            got = list(batched(inp, n, backwards=False))
            assert list(expected) == list(got)

    def test_batch_bad_iterable(self):
        with pytest.raises(TypeError): batched(345, 1)

    def test_batch_bad_n(self):
        with pytest.raises(ValueError): batched("hello", -1)
        with pytest.raises(TypeError): batched("hello", 1.3)

    def test_batch_bad_backwards_kw(self):
        with pytest.raises(TypeError): batched("hello", 1, backwards="true")

    def test_batch_bad_strict_kw(self):
        with pytest.raises(TypeError): batched("hello", 1, strict="true")
        with pytest.raises(ValueError): batched("hello", 3, strict=True)


class TestAssembler:
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
            assert expected == got

    def test_assembler_random(self):
        for i in range(10_000):
            num = randint(0, 10 ** 27)
            step = randint(1, 20)
            broken_num = break_down(num, power_step=step)
            got = assemble(broken_num)
            assert num == got

    def test_bad_assembler_input(self):
        with pytest.raises(ValueError): assemble({})
        with pytest.raises(TypeError): assemble("hello")


class TestCurrencySpeller:
    def test_bad_capitalize_kw(self):
        with pytest.raises(TypeError):
            currency_speller(number=12345, capitalize="hello", power_names=POWER_NAMES, num_names=NUM_NAMES)

    def test_too_big_number(self):
        with pytest.raises(ValueError):
            currency_speller(number=10 ** 28, power_names=POWER_NAMES, num_names=NUM_NAMES)

    def test_string_type(self):
        with pytest.raises(TypeError): currency_speller(number="123456", power_names=POWER_NAMES, num_names=NUM_NAMES)

    def test_list_type(self):
        with pytest.raises(TypeError): currency_speller(number=[123456], power_names=POWER_NAMES, num_names=NUM_NAMES)

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
            assert expected == currency_speller(num, power_names=POWER_NAMES, num_names=NUM_NAMES)

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
            499.999: "Five hundred dollars",
            520.998: "Five hundred twenty-one dollars"
        }
        for num, expected in predefined_inputs.items():
            assert expected == currency_speller(num, power_names=POWER_NAMES, num_names=NUM_NAMES)
