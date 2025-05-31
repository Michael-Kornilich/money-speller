# Money Speller

[![codecov](https://codecov.io/gh/Michael-Kornilich/money-speller/graph/badge.svg?token=GHVEBIHVUL)](https://codecov.io/gh/Michael-Kornilich/money-speller)
[![CI Pipeline](https://github.com/Michael-Kornilich/money-speller/actions/workflows/ci.yml/badge.svg)](https://github.com/Michael-Kornilich/money-speller/actions/workflows/ci.yml)

Description
---
This script is able to spell all dollar amounts of money between -10<sup>27</sup> and 10<sup>27</sup> (ends excluded)\
For example: `spell 1.234,52$` -> `One thousand two hundred thirty-four dollars and fifty-two cents`

Applications
---
* Automatic filling of documents like legal contracts and checks, that require a number be written out in words

Usage
---
In order to successfully run the script you have to have a valid `3.8+` Python version.

Run by:
1. Cloning the repository
2. (optional) Creating a new virtual environment
3. Calling `python run` (system dependent) in terminal
4. Follow the instuctions in the terminal or consult the **Description** part of the document

Quick start
---
* Run `spell <amount>` in order to spell a money amount.
* Run `separator <your-separator>`  to change the separator, which separates the integer\
or `decimal <your-decimal-separator>` to change the decimal separator.
* Run `exit` to exit the scipt.

`amount` must include the actual number as well as the currency at the end
