from typing import Dict, List, Iterable
from itertools import batched
import cmd

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


def batched_backwards(iterable: Iterable, n: int, *, strict=False) -> Iterable:
    """
    Same functionality as batched(), but starts the iteration from the back.
    I.E. batched_backwards("hello world", 3) -> "rld", " wo", "llo", "he"
    """
    iter_ = iterable[::-1]
    for i in batched(iter_, n, strict=strict): yield i[::-1]


def break_down(num: int, denominator: int) -> Dict[int, int]:
    """
    Breaks down a positive integer into {power of 10 : integer}\n
    Denominator determines the step of powers.\n
    The first power is always 0. Floats are truncated.
    """
    if not isinstance(denominator, int): raise TypeError(f"The denominator must be an integer, got {type(denominator)}")
    if not denominator >= 1: raise ValueError("The denominator must and be >= 1")

    if not isinstance(num, (float, int)): raise TypeError(f"The num must be an integer, got {type(num)}")
    if not num >= 0: raise ValueError(f"The num must be >= 0, got {num}")
    if not int(num) == num: raise ValueError(f"The num must be an integer or a float with no decimals, got {num}")

    num = int(num)

    broken_num: dict = {0: 0}
    str_num: str = str(num)

    for power, i in enumerate(batched_backwards(str_num, denominator)):
        num_chunk: int = int("".join(i))
        if num_chunk:
            broken_num.update({power * denominator: num_chunk})

    return dict(reversed(list(broken_num.items())))


def number_speller(num: int, power_names: dict, num_names: dict) -> str:
    if not isinstance(num, int): raise TypeError(f"The num must be an integer, got {type(num)}")
    if abs(num) > 10 ** 27: raise ValueError("The num must be than 1e27")

    text: List[str] = []
    num_dict: Dict[int, int] = break_down(abs(num), 3)

    for power, value in num_dict.items():
        if value < 21:
            text.append(num_names.get(value, ""))
        else:
            broken_value = break_down(value, 1)

            if v := broken_value.get(2):
                text.extend([num_names[v], power_names[2]])

            if (v := broken_value.get(1, 0) * 10 + broken_value.get(0, 0)) < 21:
                text.append(num_names.get(v, ""))
            else:
                text.append(num_names.get(broken_value[1] * 10, ""))
                text.append(num_names.get(broken_value[0], ""))

        text.append(power_names.get(power, ""))

    if num < 0:
        text.insert(0, "minus")

    return " ".join([item for item in text if item]).capitalize()


class Shell(cmd.Cmd):
    prompt = "> "
    intro = """
This script spells every integer between -10^27 and 10^27.
(Floating point numbers will be truncated)

Available functions:
    - spell: spells number(s)
    - exit: exits the script

    """

    def do_spell(self, nums):
        """
spell <number> ... <number>

Spells the numbers passed to it. 
Floating point numbers will be truncated.
To simplify the input the usage of '_' or '.' is permitted.
        """
        nums = nums.replace(".", "").split(" ")
        for num in nums:
            # guard clause
            try:
                num = int(num)
            except ValueError:
                print(f"- '{num}' is an invalid input.")
                continue

            print("- ", number_speller(num, POWER_NAMES, NUM_NAMES))

    def do_exit(self, *args):
        return 1


if __name__ == "__main__":
    Shell().cmdloop()
