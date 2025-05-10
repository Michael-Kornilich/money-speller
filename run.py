import cmd
from script import number_speller, POWER_NAMES, NUM_NAMES


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
To simplify the input, the usage of '_' or ',' is permitted.
        """
        nums = nums.replace(",", "").split(" ")
        for num in nums:
            # guard clause
            try:
                num = int(num)
            except ValueError:
                print(f"-> '{num}' is an invalid input.")
                continue

            print("-> ", number_speller(num, POWER_NAMES, NUM_NAMES))

    def do_exit(self, *args):
        return 1


if __name__ == "__main__":
    Shell().cmdloop()
