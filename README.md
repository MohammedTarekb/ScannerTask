# ScannerTask
Files of scanner project
#
This project implements a simple Lexical Analyzer and Parser in Python to tokenize and analyze basic programming syntax. The code primarily demonstrates how to parse various components of a language, identify tokens, and perform syntactic analysis for conditional and looping statements. It includes character and numeric constants, operators, keywords, identifiers, and special characters.

# Table of Contents
Requirements
Classes
Token
LexicalAnalyzer
Usage
Running the Lexer
Example Code
Sample Input and Output

# Requirements
Python 3.x
re library for regular expressions (built-in)
Classes
Token
This class represents a single token with its type and value.


class Token:
    def __init__(self, type, value):
        self.type = type  # e.g., 'KEYWORD', 'IDENTIFIER', 'NUMBER', etc.
        self.value = value  # The actual token value (e.g., 'if', 'count', '42')
LexicalAnalyzer
The LexicalAnalyzer class reads input code, breaks it down into tokens, and classifies each token as a specific type (e.g., KEYWORD, IDENTIFIER, NUMBER, OPERATOR, CHARACTER_CONSTANT, SPECIAL_CHAR, ERROR).

Key Methods
advance(): Moves to the next character in the input.
is_whitespace(), is_letter(), is_digit(), is_operator(): Helpers to identify characters.



get_next_token(): Identifies and returns the next token in the input
