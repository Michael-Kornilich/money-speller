import cmd
from script import number_speller, POWER_NAMES, NUM_NAMES


class Shell(cmd.Cmd):
    prompt = "> "
    intro = """
    This script spells every integer between -10^27 and 10^27.
    (Floating point numbers will be truncated)

    Available functions:
        - spell <number>: spells number(s)
        - exit: exits the script
    """

    def do_spell(self, num):
        """
        spell <number>
        Spells the numbers passed to it.
        Floating point numbers will be truncated.
        To simplify the input, the usage of "_", " ", "," is permitted to separate the number.
        """

        num = num.replace(",", "").replace(" ", "")

        try:
            num = float(num)
        except ValueError:
            print(f"-> '{num}' is an invalid input.")

        # for testing purposes
        # return num
        print("-> ", number_speller(num, power_names=POWER_NAMES, num_names=NUM_NAMES))

    def do_exit(self, *args):
        return 1


if __name__ == "__main__":
    Shell().cmdloop()
