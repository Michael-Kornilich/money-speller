import cmd
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


def get_time_of_day() -> str:
    """
    Helper function for dynamic greetings.
    :return: "morning" | "day" | "afternoon" | "evening" | "night"
    """
    from datetime import datetime
    hour = datetime.now().time().hour

    if 23 <= hour or hour < 4:
        return "night"
    elif 4 <= hour <= 12:
        return "morning"
    elif 12 < hour <= 17:
        return "afternoon"
    else:
        return "evening"


def parse_num(str_: str, /, *, separator: str = ",", decimal: str = ".") -> float | None:
    """
    Parses any number of the form:\n
    [0-9$]+<separator>[0-9$]+....<decimal>[0-9$]+
    :param str_: the number to be parsed as string
    :param separator: the separator to use while parsing
    :param decimal: the decimal separator to use while parsing
    :returns: float if parsing is successful, None if failed
    """
    if "$" not in str_: return None

    string = str_.replace(separator, "").replace(decimal, ".").replace("$", "")

    try:
        return float(string)
    except ValueError:
        return None


class Shell(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.available_sep = [',', '.', '-', '–', '_', '&', '/', ':', '|']
        self.separator = "."
        self.decimal = ","

    prompt = "> "
    intro = """
    Good {time}!
    This script spells every money amount between -10^27 and 10^27 (ends excluded).

    \033[94mAvailable functions\033[0m:
    
        -\033[92m spell <amount>\033[0m: 
            Spell the <amount> of money
        
        -\033[92m separator [<new-separator>]\033[0m: 
            Define a separator, which is used to split the whole parts of the numbers.
            If nothing passed show the current separator.
            The available separators are as follow:
                {sep_list}   
            The default separator is "."
            The separator is not strictly enforced, so calling ..$...1....4 will work the same as calling $14.
            
        -\033[92m decimal [<new-decimal-separator>]\033[0m: 
            Define a decimal separator.
            The available separators are as follow:
                {sep_list} 
            The default one is ",".
            If nothing passed show the current decimal separator.
            The decimal separator is used to split the integer from its decimal part. 
            It is STRICTLY enforced and the spelling will fail
            if the decimal separator is found in the target number more than once.
            
        -\033[92m exit\033[0m: 
            Exits the script
    """.format(time=get_time_of_day(), sep_list=" ".join([',', '.', '-', '–', '_', '&', '/', ':', '|']))

    def do_separator(self, sep: str):
        """
        Set a new integer separator or see the current one (if nothing passed)
        """
        if not sep:
            print(f"Current integer separator: '{self.separator}'")
            return

        if sep not in self.available_sep:
            print(f"Invalid integer separator '{sep}'.\n"
                  f"The available integer separators are: {" ".join(self.available_sep)}")
            return
        if sep == self.decimal:
            print(f"Invalid integer separator '{sep}'. The integer and the decimal separators cannot be same.")
            return

        self.separator = sep
        print(f"Changed separator to: {sep}")

    def do_decimal(self, dec: str):
        """
        Set a new decimal separator or see the current one (if nothing passed)
        """
        if not dec:
            print(f"Current decimal separator: '{self.decimal}'")
            return

        if dec not in self.available_sep:
            print(f"Invalid decimal separator '{dec}'.\n"
                  f"The available decimal separators are: {" ".join(self.available_sep)}")
            return
        if dec == self.separator:
            print(f"Invalid decimal separator '{dec}'. The decimal and the integer separators cannot be same.")
            return

        if len(dec) == 0:
            print(f"Current separator: {self.decimal}")
        elif len(dec) == 1:
            self.decimal = dec
            print(f"Changed separator to: {dec}")

    def do_spell(self, _num: str):
        """
        spell <number>
        Spells the numbers passed to it.
        Money amounts with more than 2 decimals will be rounded to 2 decimals
        To simplify the input, the usage of "_" and the defined separator is permitted to separate the number.
        """
        from script import currency_speller

        num: float | None = parse_num(_num, separator=self.separator, decimal=self.decimal)
        if not num:
            print("Invalid input.")
            return

        print("-> " + currency_speller(num, num_names=NUM_NAMES, power_names=POWER_NAMES))

    def do_exit(self, *args):
        """
        Exit the script
        """
        return 1


if __name__ == "__main__":
    Shell().cmdloop()
