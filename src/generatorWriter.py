#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ast import NodeVisitor, Name, Yield


class GeneratorWriter(NodeVisitor):

    def __init__(self, codeGenerator):
        self.codeGenerator = codeGenerator


    def generic_visit(self, node):
        self.codeGenerator.visit(node)

    class SearchReturn(NodeVisitor):

        def __init__(self, node):
            self.ret = None
            self.visit(node)

        def visit_Return(self, node):
            self.ret = node

        def getReturn(self):
            return self.ret


    def visit_FunctionDef(self, t):

        name = t.name

        # include directives
        self.codeGenerator.includes.add("generator.h")
        self.codeGenerator.includes.add("coroutine.h")
        self.codeGenerator.includes.add("yield.h")


        self.codeGenerator.output.fill()
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


        self.codeGenerator.output.fill("coroutine c;")
        self.codeGenerator.output.fill("return Generator<long int>([=]() mutable -> long int")

        self.codeGenerator.enterScope()
        self.codeGenerator.output.fill("reenter(c)")
        self.codeGenerator.enterScope()
        self.visit(t.body)

        self.codeGenerator.leaveScope(None, "")
        self.codeGenerator.output.fill("throw EndOfGenerator();")
        self.codeGenerator.leaveScope(None, ");")
        self.codeGenerator.leaveScope(t)

        tmpBuffer = self.codeGenerator.output.topPop()

        ### Finds the return type
        returnFinder = self.SearchReturn(t)
        self.codeGenerator.output.write("Generator<")
        if returnFinder.getReturn():
            typeFinder = self.ReturnTypeFinder(t)
            self.codeGenerator.output.write(
                typeFinder.getType(returnFinder.getReturn(),
                                   self.codeGenerator))
        else:
            self.codeGenerator.output.write("void")
        self.codeGenerator.output.write(">")

        self.codeGenerator.output.write(tmpBuffer.getvalue())
