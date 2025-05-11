import cmd
from script import number_speller, POWER_NAMES, NUM_NAMES


def _parse_num(str_: str, /, *, separator: str = ",", decimal: str = ".") -> int | float:
    """
    Raises a ValueError if parsing failed
    """
    string = str_.replace(separator, "").replace(decimal, ".")

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
        - exit: exits the script
    """

    def __init__(self):
        super().__init__()
        self.separator = ","
        self.decimal = "."

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
            print(f"Current separator: {self.separator}")
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
        To simplify the input, the usage of "_", " ", "," is permitted to separate the number.
        """
        try:
            num_ = _parse_num(num, separator=self.separator, decimal=self.decimal)
        except ValueError:
            print("Invalid input.")
            return

        print("-> ", number_speller(num_, power_names=POWER_NAMES, num_names=NUM_NAMES))

    def do_exit(self, *args):
        return 1


if __name__ == "__main__":
    Shell().cmdloop()
