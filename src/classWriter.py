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
        if isinstance(node, list):
            for n in node:
                self.codeGenerator.visit(n)
        else:
            self.codeGenerator.visit(node)


    def visit_ClassDef(self, t):
        self.codeGenerator.output.stackBuffer()
        self.codeGenerator.output.write("\n")

        self.codeGenerator.output.fill("class " + t.name)

        #for decorator in t.decorator_list:
        #    print(decorator)

        #for base in t.bases:
        #    print(base)

        #for keyword in t.keywords:
        #    print(keyword)


        for stmt in t.body:
            self.codeGenerator.visit(stmt)

        self.codeGenerator.output.flushLastInFile(t.name + ".h")
        self.codeGenerator.includes.add(t.name + ".h")
