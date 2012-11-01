#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codeGenerator import CodeGenerator
from outputManager import outputManager as CodeFormatter

import sys
import ast

def parse(filename):
    """
    Parse the given file and write the result of conversion
    into output (default to stdout)
    """

    # read source file
    with open(filename, "r") as pyfile:
        source = pyfile.read()

    # Build the abstract syntax tree
    tree = compile(source, filename, "exec", ast.PyCF_ONLY_AST)

    formatter = CodeFormatter()

    generator = CodeGenerator(formatter)
    generator.visit(tree)

    formatter.flush()



def main(args):
    for f in args:
        parse(f)

if __name__=='__main__':
    main(sys.argv[1:])
