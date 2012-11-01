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
        self.className = ""


    def visit_FunctionDef(self, node):
        # Constructor
        if node.name == "__init__":
            node.name = self.className
            # TODO
        self.codeGenerator.visit(node)



    def visit_ClassDef(self, t):
        self.codeGenerator.output.stackBuffer()
        self.className = t.name
        self.codeGenerator.output.write("\n")

        self.codeGenerator.output.fill("class " + t.name)
        self.codeGenerator.output.enter()

        #for decorator in t.decorator_list:
        #    print(decorator)

        #for base in t.bases:
        #    print(base)

        #for keyword in t.keywords:
        #    print(keyword)


        for stmt in t.body:
            self.codeGenerator.visit(stmt, self)

        self.codeGenerator.output.leave()
        self.codeGenerator.output.write(";")

        self.codeGenerator.output.flushLastInFile(t.name + ".h")
        self.codeGenerator.includes.add(t.name + ".h")
