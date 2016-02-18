#!/usr/bin/python
#
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
#

import sys
import time


def execute(filename):
    f = open(filename, "r")
    evaluate(f.read())
    f.close()


def evaluate(code, timeout=5):
    """
    Modified brainfuck interpreter based on https://github.com/pocmo/Python-Brainfuck/blob/master/brainfuck.py

    Executes string of brainfuck code and returns a string of output

    Has a timeout function to limit execution time.

    Disabled user input for now... could be fed some kind of input buffer
    in the future.

    """
    output = ""
    code = cleanup(list(code))
    bracemap = buildbracemap(code)

    cells, codeptr, cellptr = [0], 0, 0

    start = time.time()
    while (time.time() - start < timeout) and (codeptr < len(code)):
        command = code[codeptr]
        if command == ">":
            cellptr += 1
            if cellptr == len(cells):
                cells.append(0)
        if command == "<":
            cellptr = 0 if cellptr <= 0 else cellptr - 1
        if command == "+":
            cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0
        if command == "-":
            cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255
        if command == "[" and cells[cellptr] == 0:
            codeptr = bracemap[codeptr]
        if command == "]" and cells[cellptr] != 0:
            codeptr = bracemap[codeptr]
        if command == ".":
            output += chr(cells[cellptr])
        ##if command == ",": cells[cellptr] = ord(getch())

        codeptr += 1

    return output


def cleanup(code):
    return list(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))


def buildbracemap(code):
    temp_bracestack, bracemap = [], {}

    for position, command in enumerate(code):
        if command == "[":
            temp_bracestack.append(position)
        if command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start
    return bracemap
