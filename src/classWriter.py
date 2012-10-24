#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ast import NodeVisitor


class ClassWriter(NodeVisitor):
    """
    """

    def __init__(self, codeGenerator):
        """
        """
        self.codeGenerator = codeGenerator


    def generic_visit(self, node):
        """ """
        self.codeGenerator.visit(node)


    def visit_ClassDef(self, t):
        self.output.write("\n")
        #for deco in t.decorator_list:
            #    self.output.fill("@")
            #    self.visit(deco)
        self.output.fill("class " + t.name)
        if t.bases:
            self.output.write(": ")
            for a in t.bases:
                self.output.write("public ")
                self.visit(a)
                self.output.write(", ")
                self.output.write("\n")
                self.output.enter()
                self.visit(t.body)
                self.output.leave()
                self.output.write(";")
