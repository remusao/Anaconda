#!/usr/bin/env python
# -*- coding: utf-8 -*-


def parse(filename, output = sys.stdout):
    """
    Parse the given file and write the result of conversion
    into output (default to stdout)
    """

    # read source file
    with open(filename, "r") as pyfile:
        source = pyfile.read()

    buffer = cStringIO.StringIO()

    # Build the abstract syntax tree
    tree = compile(source, filename, "exec", ast.PyCF_ONLY_AST)

    ###  Refactor and output C++ into buffer ###
    unparser = Unparser(tree, buffer)


    # Write mandatory includes
    for include in unparser.includes:
        output.write("#include <%s>\n" % include)

    output.write(buffer.getvalue())





# If it's exec directly


def main(args):
    for f in args:
        parser.parse(file)

if __name__=='__main__':
    main(sys.argv[1:])
