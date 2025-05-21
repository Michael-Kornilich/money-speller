import cmd
from script import currency_speller
from typing import Dict

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


def parse_num(str_: str, /, *, separator: str = ",", decimal: str = ".") -> int | float:
    """
    Raises a ValueError if parsing failed
    """
    if "$" not in str_: raise ValueError("Failed to parse the amount, no currency sign.")

    string = str_.replace(separator, "").replace(decimal, ".").replace("$", "")

    try:
        return float(string)
    except ValueError:
        raise ValueError("The number could not be parsed")


class Shell(cmd.Cmd):
    prompt = "> "
    intro = """
    This script spells every integer between -10^27 and 10^27.
    (Floating point numbers will be truncated)

    Available functions:
        - spell <number>: spells number(s)
        - separator <new separator or nothing>: 
            Default = "."
            define a separator which is used to split the whole parts of the numbers.
            The separator is not strictly enforced so calling 1......4 will return fourteen.
        - decimal <new decimal separator or nothing>: 
            Default = ","
            define a decimal separator. 
            The decimal separator is used to split the integer from its decimal part. 
            It IS strictly enforced and the spell function will not work
            if the decimal separator is found in the target number more than once.
        - exit: exits the script
    """

    def __init__(self):
        super().__init__()
        self.separator = "."
        self.decimal = ","

    def do_separator(self, sep):
        if len(sep) == 0:
            print(f"Current separator: {self.separator}")
        elif len(sep) == 1:
            self.separator = sep
            print(f"Changed separator to: {sep}")
        else:
            print(f"Invalid input {sep}. Pass a single character to change the separator or "
                  f"nothing in order to view the current separator")

    def do_decimal(self, dec):
        if len(dec) == 0:
            print(f"Current separator: {self.decimal}")
        elif len(dec) == 1:
            self.decimal = dec
            print(f"Changed separator to: {dec}")
        else:
            print(f"Invalid input {dec}. Pass a single character to change the decimal separator or "
                  f"nothing in order to view the current decimal separator")

    def do_spell(self, num: str):
        """
        spell <number>
        Spells the numbers passed to it.
        Floating point numbers will be truncated.
        To simplify the input, the usage of "_" and the defined separator is permitted to separate the number.
        """
        try:
            num_ = parse_num(num, separator=self.separator, decimal=self.decimal)
        except ValueError:
            print("Invalid input.")
            return

        print("-> ", currency_speller(num_, num_names=NUM_NAMES, power_names=POWER_NAMES))

    def do_exit(self, *args):
        return 1


if __name__ == "__main__":
    Shell().cmdloop()
