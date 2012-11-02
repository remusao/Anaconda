#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ast import NodeVisitor, Name, Yield


class GeneratorWriter(NodeVisitor):

    def __init__(self, codeGenerator):
        self.codeGenerator = codeGenerator


    def generic_visit(self, node):
        self.codeGenerator.visit(node)



    def visit_FunctionDef(self, t):

        name = t.name

        # include directives
        self.codeGenerator.includes.add("generator.h")
        self.codeGenerator.includes.add("coroutine.h")

        # Create the generator class
        self.codeGenerator.output.fill("class %s" % (name))
        self.codeGenerator.enterScope()

        # Create constructors
        self.codeGenerator.output.fill("%s(")
        nbArgs = len(t.args.args)
        if nbArgs > 0:
            self.codeGenerator.output.write("template <")
            for e in range(0, nbArgs - 1):
                self.codeGenerator.output.write("typename Type%i" % (e))
                self.codeGenerator.output.write(", ")
            self.codeGenerator.output.write("typename Type%i>" % (nbArgs - 1))
        self.codeGenerator.output.fill("auto " + t.name + "(")
        self.codeGenerator.visit(t.args)
        self.codeGenerator.output.write(") -> ")

        ### output.write body to a temporary buffer

        self.codeGenerator.output.stackBuffer()
        self.codeGenerator.enterScope()

        self.visit(t.body)

        self.codeGenerator.leaveScope(t)

        tmpBuffer = self.codeGenerator.output.topPop()

        ### Finds the return type
        returnFinder = self.SearchReturn(t)
        if returnFinder.getReturn():
            typeFinder = self.ReturnTypeFinder(t)
            self.codeGenerator.output.write(
                typeFinder.getType(returnFinder.getReturn(),
                                   self.codeGenerator))
        else:
            self.codeGenerator.output.write("void")

        self.codeGenerator.output.write(tmpBuffer.getvalue())
