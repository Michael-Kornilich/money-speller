from random import randint

class ApplicationParserTests():

    def test_underscores(self):
        expected = 1234
        got = parse_num("1_2_3_4$")
        self.assertEqual(expected, got)

    def test_leading_0s(self):
        expected = 1234
        got = parse_num("0001234$")
        self.assertEqual(expected, got)

    def test_bad_input(self):
        bad_inputs = [
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
        ]

        for inp in bad_inputs:
            self.assertEqual(None, parse_num(inp))

    def test_bad_random_input(self):
        for _ in range(10_000):
            chars = "".join(chr(randint(0, 1_114_111)) for i in range(10))
            if not chars.isnumeric():
                self.assertEqual(None, parse_num(chars))

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
            self.assertEqual(exp, split_decimal(inp))


class ApplicationSeparatorsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shell = Shell()
        cls.integer_sep = cls.shell.integer_sep
        cls.decimal_sep = cls.shell.decimal_sep

    @patch("builtins.print")
    def test_decimal_bad_input(self, mock_print):
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
            mock_print.assert_called_with(
                f"Invalid decimal separator '{val}'.\n"
                f"The available decimal separators are: {" ".join(self.shell.available_sep)}")

    @patch("builtins.print")
    def test_decimal_special(self, mock_print):
        io = {
            self.integer_sep: "Switched the separators around.\n"
                              f"New decimal separator: {self.integer_sep}\n"
                              f"New integer separator: {self.decimal_sep}",
        }
        for dec, err_msg in io.items():
            self.shell.do_decimal(dec)
            mock_print.assert_called_with(err_msg)

    @patch("builtins.print")
    def test_separator(self, mock_print):
        bad_inputs = [
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
        ]

        for val in bad_inputs:
            self.shell.do_separator(val)
            mock_print.assert_called_with(
                f"Invalid integer separator '{val}'.\n"
                f"The available integer separators are: {" ".join(self.shell.available_sep)}")

    @patch("builtins.print")
    def test_separator_special(self, mock_print):
        io = {
            self.decimal_sep: "Switched the separators around.\n"
                              f"New decimal separator: {self.integer_sep}\n"
                              f"New integer separator: {self.decimal_sep}",
        }
        for dec, err_msg in io.items():
            self.shell.do_decimal(dec)
            mock_print.assert_called_with(err_msg)