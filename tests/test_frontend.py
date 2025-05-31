from random import randint
import pytest
from scripts.app import *
from scripts.script import split_decimal


class TestApplicationParser:
    def test_underscores(self):
        expected = 1234
        got = parse_num("1_2_3_4$")
        assert expected == got

    def test_leading_0s(self):
        expected = 1234
        got = parse_num("0001234$")
        assert expected == got

    def test_bad_input(self):
        bad_inputs = (
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
            "-",
            "√asdg"
        )

        for inp in bad_inputs:
            assert None == parse_num(inp)

    def test_bad_random_input(self):
        for _ in range(10_000):
            chars = "".join(chr(randint(0, 1_114_111)) for i in range(10))
            if not chars.isnumeric():
                assert None == parse_num(chars)

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
            assert exp == split_decimal(inp)


class TestApplicationSeparators:
    @classmethod
    def setup_class(cls):
        cls.shell = Shell()

    def test_decimal_bad_input(self, capsys):
        bad_inputs = [
            "hello",
            "six"
            "324md",
            "\033fdfl",
            "\n",
            "\r",
            "---",
            "\\",
            "\thello"
        ]

        for val in bad_inputs:
            self.shell.do_decimal(val)

            captured = capsys.readouterr()
            assert captured.out == (f"Invalid decimal separator '{val}'.\n"
                                    f"The available decimal separators are: {" ".join(self.shell.available_sep)}\n")

    def test_decimal_special(self, capsys):
        io = {
            self.shell.integer_sep: "Switched the separators around.\n"
                                    f"New decimal separator: {self.shell.integer_sep}\n"
                                    f"New integer separator: {self.shell.decimal_sep}\n",
        }
        for dec, err_msg in io.items():
            self.shell.do_decimal(dec)

            captured = capsys.readouterr()
            assert captured.out == err_msg

    def test_separator(self, capsys):
        bad_inputs = (
            "hello",
            "5",
            "9"
            "six"
            "324md",
            "\033fdfl",
            "---",
            "        "
            "\n",
            "\r"
        )

        for val in bad_inputs:
            self.shell.do_separator(val)
            captured = capsys.readouterr()
            assert captured.out == (f"Invalid integer separator '{val}'.\n"
                                    f"The available integer separators are: {" ".join(self.shell.available_sep)}\n")

    def test_separator_special(self, capsys):
        io = {
            self.shell.decimal_sep: "Switched the separators around.\n"
                                    f"New decimal separator: {self.shell.integer_sep}\n"
                                    f"New integer separator: {self.shell.decimal_sep}\n",
        }
        for dec, msg in io.items():
            self.shell.do_separator(dec)
            captured = capsys.readouterr()
            assert captured.out == msg


class TestApplicationSpeller:
    @classmethod
    def setup_class(cls):
        cls.shell = Shell()

    def test_bad_inputs(self, capsys):
        bad_inputs = (
            "123",
            "hello",
            "\n",
            "\t",
            "√å‚∂«∑€",
            "123g$",
            "-123d$",
            "",
            "-\321$",
            "Minus 123$",
        )
        for val in bad_inputs:
            self.shell.do_spell(val)
            captured = capsys.readouterr()
            assert captured.out == "Invalid input.\n"


class TestSeparatorChanger:
    @classmethod
    def setup_class(cls):
        cls.shell = Shell()

    def teardown_sep(self):
        self.shell.integer_sep = "."
        self.shell.decimal_sep = ","

    def test_simple_decimal_change(self):
        for inp in self.shell.available_sep:
            self.shell._change_separator(new_sep=inp, _tp="decimal")
            assert self.shell.decimal_sep == inp
        self.teardown_sep()

    def test_simple_integer_change(self):
        for inp in self.shell.available_sep:
            self.shell._change_separator(new_sep=inp, _tp="integer")
            assert self.shell.integer_sep == inp
        self.teardown_sep()

    def test_switch_integer(self):
        self.shell._change_separator(
            new_sep=self.shell.decimal_sep,
            _tp="integer")

        assert self.shell.integer_sep == ","
        assert self.shell.decimal_sep == "."
        self.teardown_sep()

    def test_switch_decimal(self):
        self.shell._change_separator(
            new_sep=self.shell.integer_sep,
            _tp="decimal")

        assert self.shell.integer_sep == ","
        assert self.shell.decimal_sep == "."
        self.teardown_sep()

    def test_empty_integer_sep(self):
        got = self.shell._change_separator(new_sep="", _tp="integer")
        assert f"Current integer separator: '{self.shell.integer_sep}'" == got
        self.teardown_sep()

    def test_empty_decimal_sep(self):
        got = self.shell._change_separator(new_sep="", _tp="decimal")
        assert f"Current decimal separator: '{self.shell.decimal_sep}'" == got
        self.teardown_sep()

    def test_invalid_integer_sep(self):
        bad_seps = (
            "hello",
            "1",
            "...",
            ",.,.",
            "\n",
            ",5",
            "0",
            "\\",
            "\t"
        )
        for val in bad_seps:
            got = self.shell._change_separator(new_sep=val, _tp="integer")
            assert got == (f"Invalid integer separator '{val}'.\n"
                           f"The available integer separators are: {" ".join(self.shell.available_sep)}")
        self.teardown_sep()

    def test_invalid_decimal_sep(self):
        bad_seps = (
            "hello",
            "1",
            "...",
            ",.,.",
            "\n",
            ",5",
            "0",
            "\\",
            "\t"
        )
        for val in bad_seps:
            got = self.shell._change_separator(new_sep=val, _tp="decimal")
            assert got == (f"Invalid decimal separator '{val}'.\n"
                           f"The available decimal separators are: {" ".join(self.shell.available_sep)}")
        self.teardown_sep()


class TestMiscellaneous:
    @classmethod
    def setup_class(cls):
        cls.shell = Shell()

    def test_exit(self):
        for _ in range(100):
            assert 1 == self.shell.do_exit(randint(-100, 100))

    def test_get_datetime(self):
        bad_inp = [
            "hello",
            "",
            "123",
            "\n",
            None
        ]
        for val in bad_inp:
            with pytest.raises(TypeError): get_time_of_day(val)
