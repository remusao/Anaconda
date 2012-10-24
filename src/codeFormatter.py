#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stdout
from io import StringIO


class CodeFormatter():
    """
    """

    def __init__(self, outputStream = stdout):
        """
        """
        self.f = [outputStream]
        self._indent = 0


    def stackBuffer(self):
        self.f.append(StringIO())


    def popBuffer(self):
        del self.f[-1]


    def topBuffer(self):
        return self.f[-1]


    def mergeLastBuffer(self):
        self.f[-2].write(self.f[-1].getvalue())
        self.popBuffer()


    def fill(self, text = ""):
        """
        Indent a piece of text, according to the current indentation level
        """
        self.topBuffer().write("\n" + "    " * self._indent + text)

    def write(self, text):
        "Append a piece of text to the current line."
        self.topBuffer().write(text)

    def enter(self):
        "Print ':', and increase the indentation."
        self.topBuffer().write("\n{")
        self._indent += 1

    def leave(self):
        "Decrease the indentation level."
        self.topBuffer().write('\n}\n')
        self._indent -= 1



    def flush(self):
        """
        """
        pass
