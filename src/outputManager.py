#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stdout
from io import StringIO


class outputManager():
    """
    """

    def __init__(self, outputStream = stdout):
        """
        """
        self.f = [StringIO()]
        self.outputStream = outputStream
        self._indent = 0


    def stackBuffer(self):
        self.f.append(StringIO())


    def pushBuffer(self, buffer):
        self.f.append(buffer)


    def topPop(self):
        tmp = self.topBuffer()
        self.popBuffer()
        return tmp

    def popBuffer(self):
        del self.f[-1]


    def topBuffer(self):
        return self.f[-1]


    def mergeLastBuffer(self):
        self.f[-2].write(self.f[-1].getvalue())
        self.popBuffer()

    def flushLastInFile(self, fileName):
        with open(fileName, 'w') as of:
            of.write(self.f[-1].getvalue())
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
        self.topBuffer().write("\n%s{" % ("    " * self._indent))
        self._indent += 1

    def leave(self):
        "Decrease the indentation level."
        self._indent -= 1
        self.topBuffer().write("\n%s}\n" % ("    " * self._indent))



    def flush(self):
        for s in self.f:
            self.outputStream.write(s.getvalue())
