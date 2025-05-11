from typing import Dict, List, Iterable

# TODO
# test the number speller and the parser extensively
# add float spelling
# add money spelling
# add a csv with
# name, currency_major, currency_minor, decimal, separator
# ...
# add the test coverage badge
# build a CI pipeline with the tests
# reduce the dependency on the NUM_NAMES and POWER_NAMES

NUM_NAMES: Dict[int, str] = {
    # 0: '',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety'
}
POWER_NAMES: Dict[int, str] = {
    2: "hundred",
    3: "thousand",
    6: "million",
    9: "billion",
    12: "trillion",
    15: "quadrillion",
    18: "quintillion",
    21: "hexillion",
    24: "heptillion"
}


def batched(iterable: Iterable, n: int, *, strict=False, backwards: bool = False) -> Iterable:
    """
    Same functionality as itertools.batched, but with an added feature of iteration backwards.
    I.E.
    batched("hello world", 3, backwards=False) -> "hel", "lo ", "wor", "ld"
    batched("hello world", 3, backwards=True) -> "rld", " wo", "llo", "he"
    """
    from itertools import islice

    if n < 1: raise ValueError(f'n must be at least one, got {n}')
    if not isinstance(backwards, bool):
        raise TypeError(f"Keyword backwards must be a boolan value, got {type(backwards)}")

    iterator = iter(iterable[::-1]) if backwards else iter(iterable)

    while batch := tuple(islice(iterator, n)):
        if strict and len(batch) != n:
            raise ValueError('batched(): strict=True, incomplete batch')

        if backwards:
            yield batch[::-1]
        else:
            yield batch


def break_down(num: int, power_step: int) -> Dict[int, int]:
    """
    Breaks down a positive integer into {power of 10 : integer}\n
    power_step determines the step of powers.\n
    The first power is always 0. Floats are truncated.
    """
    if not isinstance(power_step, int): raise TypeError(f"The power_step must be an integer, got {type(power_step)}")
    if not power_step >= 1: raise ValueError("The power_step must and be >= 1")

    if not isinstance(num, (float, int)): raise TypeError(f"The num must be an integer, got {type(num)}")
    if not num >= 0: raise ValueError(f"The num must be >= 0, got {num}")
    if not int(num) == num: raise ValueError(f"The num must be an integer or a float with no decimals, got {num}")

    num = int(num)

    broken_num: dict = {0: 0}
    str_num: str = str(num)

    for power, i in enumerate(batched(str_num, power_step, backwards=True)):
        num_chunk: int = int("".join(i))
        if num_chunk:
            broken_num.update({power * power_step: num_chunk})

    return dict(reversed(list(broken_num.items())))


def assemble(broken_value: Dict[int, int], /) -> int:
    if not isinstance(broken_value, dict): raise TypeError(f"Expected a dictionary, got {type(broken_value)}")
    if not broken_value: raise ValueError("The broken value must have values inside")

    res = 0
    for power, value in broken_value.items():
        res += (10 ** power) * value
    return res


def number_speller(num: int, power_names: dict, num_names: dict) -> str:
    if not isinstance(num, int): raise TypeError(f"The num must be an integer, got {type(num)}")
    if abs(num) >= 10 ** 27: raise ValueError("The |num| must be less than 1e27")

    if num < 0:
        text: List[str] = ["minus"]
    else:
        text: List[str] = []

    num_dict: Dict[int, int] = break_down(abs(num), 3)

    for power, value in num_dict.items():
        if not value: continue

        broken_value = break_down(value, 1)

        # extracting 100s
        if assemble(broken_value) >= 100:
            hundreds = broken_value[2]
            text.extend([num_names[hundreds], power_names[2]])
            broken_value.pop(2)

        # extracting 10s
        if 21 <= assemble(broken_value) <= 99:
            text.append(num_names[broken_value[1] * 10])
            # 0s are not in the NUM_NAMES, so raw indexing might error out
            text.append(num_names.get(broken_value[0], ""))

        # special 0-20
        else:
            v = assemble(broken_value)
            # 0s are not in the NUM_NAMES, so raw indexing might error out
            text.append(num_names.get(v, ""))

        # powers 0, 1 are not in the POWER_NAMES
        text.append(power_names.get(power, ""))

    return " ".join([item for item in text if item]).capitalize()
