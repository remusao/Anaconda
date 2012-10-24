#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ast import NodeVisitor


class FunctionWriter(NodeVisitor):
    """
    """

    def __init__(self, codeGenerator):
        """ """
        self.codeGenerator = codeGenerator


    def generic_visit(self, node):
        """  """
        self.codeGenerator.visit(node)


    # TODO
    def visit_FunctionDef(self, t):
        self.codeGenerator.output.write("\n")
        nbArgs = 0 #len(t.args.args)
        if nbArgs > 0:
            self.codeGenerator.output.write("template <")
            for e in range(0, nbArgs - 1):
                self.codeGenerator.output.write("typename Type%i" % (e))
                self.codeGenerator.output.write(", ")
            self.codeGenerator.output.write("typename Type%i>" % (nbArgs - 1))
        self.codeGenerator.output.fill("auto " + t.name + "(")
        self.codeGenerator.visit(t.args)
        self.codeGenerator.output.write(") -> ")

        # Trace the assignements in the function body
        assignements = []

        ### output.write body to a temporary buffer

        self.codeGenerator.output.stackBuffer()

        self.codeGenerator.output.enter()
        for node in t.body:
            self.visit(node)
        self.codeGenerator.output.leave()

        ### Finds the return type
        body = {x.__class__.__name__ : x for x in t.body}
        if "Return" in body:
            self.codeGenerator.output.write(findReturnType(body["Return"], assignements))
        else:
            self.codeGenerator.output.write("void")

        self.codeGenerator.output.mergeLastBuffer
