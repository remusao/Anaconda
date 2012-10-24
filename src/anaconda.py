#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codeGenerator import CodeGenerator
from codeFormatter import CodeFormatter

import sys
import ast

def parse(filename, output = sys.stdout):
    """
    Parse the given file and write the result of conversion
    into output (default to stdout)
    """

    # read source file
    with open(filename, "r") as pyfile:
        source = pyfile.read()


    # Build the abstract syntax tree
    tree = compile(source, filename, "exec", ast.PyCF_ONLY_AST)

    formatter = CodeFormatter(output)
    generator = CodeGenerator(formatter)
    generator.visit(tree)

    ###  Refactor and output C++ into buffer ###
    #unparser = Unparser(tree, buffer)


    formatter.flush()





# If it's exec directly


def main(args):
    for f in args:
        parse(f)

if __name__=='__main__':
    main(sys.argv[1:])
