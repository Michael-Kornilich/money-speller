# i.e. 2.013.777,34 -> f(x) -> two million thirteen thousand seven hundred seventy-seven and thirty-four
from typing import Dict, List
from itertools import batched
import sys

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


def break_down(num: int, denominator: int) -> Dict[int, int]:
    """
    Breaks down a positive integer into {power of 10 : integer}\n
    Denominator determines the step of powers.\n
    The first power is always 0
    """
    if (type(denominator) is not int) or (denominator < 1):
        raise ValueError("The denominator must and be a positive integer")

    if (
            (type(num) in [float, int]) and
            (num >= 0) and
            (int(num) == num)
    ):
        num = int(num)

        broken_num: dict = {0: 0}
        str_num: str = str(num)[::-1]

        for power, i in enumerate(batched(str_num, denominator)):
            num_chunk: int = int(''.join(i)[::-1])

            if not num_chunk: continue

            broken_num.update({power * denominator: num_chunk})

        return dict(reversed(list(broken_num.items())))
    else:
        raise ValueError("The num must be a positive integer or zero")


def number_speller(num: int, power_names: dict, num_names: dict) -> str:
    if (type(num) is not int) or abs(num) > 10 ** 27:
        raise ValueError("The |num| must and be an integer smaller than 1e27")

    text: List[str] = []

    if num < 0:
        text.append("minus")
        num = abs(num)

    num_dict: Dict[int, int] = break_down(num, 3)

    for power, value in num_dict.items():
        if value < 21:
            text.append(num_names.get(value, ""))
            text.append(power_names.get(power, ""))
            continue

        broken_value = break_down(value, 1)

        if broken_value.get(2):
            text.extend([num_names[broken_value[2]], power_names[2]])

        if broken_value.get(1):
            text.append(num_names[broken_value.get(1, 0) * 10])

        if broken_value.get(0):
            text.append(num_names[broken_value[0]])

        text.append(power_names.get(power, ""))

    return " ".join(text).capitalize()


print(number_speller(145214, POWER_NAMES, NUM_NAMES))

# try:
#     n = float(sys.argv[1])
# except ValueError:
#     raise ValueError("The |num| must and be an integer smaller than 1e27")
#
# if int(n) == n:
#     print(number_speller(int(n), POWER_NAMES, NUM_NAMES))
