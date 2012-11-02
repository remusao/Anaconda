#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ast import NodeVisitor, Name
from generatorWriter import GeneratorWriter


class FunctionWriter(NodeVisitor):
    """
    """

    def __init__(self, codeGenerator):
        """ """
        self.codeGenerator = codeGenerator
        self.generatorWriter = GeneratorWriter(codeGenerator)


    def generic_visit(self, node):
        """  """
        self.codeGenerator.visit(node)


    def outputMain(self, node):
        self.codeGenerator.output.write("int main(")
        self.visit(node.args)
        self.codeGenerator.output.write(")")
        self.codeGenerator.enterScope()
        self.visit(node.body)
        self.codeGenerator.leaveScope(node)


    class ReturnTypeFinder(NodeVisitor):

        def __init__(self, node):
            self.assignements = []
            self.visit(node)

        def visit_Assign(self, node):
            """"""
            #print(node)
            for target in node.targets:
                if isinstance(target, Name):
                    self.assignements += (target.id, node.value)


        def getType(self, returnStmt, visitor):
            type = 'void'
            if returnStmt.value:
                visitor.output.stackBuffer()
                visitor.visit(returnStmt.value)
                type = visitor.output.topPop().getvalue()
            return "decltype(%s)" % (type)



    class SearchYield(NodeVisitor):

        def __init__(self, node):
            self.y = None
            self.visit(node)

        def visit_Yield(self, node):
            self.y = node

        def getYield(self):
            return self.y


    class SearchReturn(NodeVisitor):

        def __init__(self, node):
            self.ret = None
            self.visit(node)

        def visit_Return(self, node):
            self.ret = node

        def getReturn(self):
            return self.ret


    # TODO
    def visit_FunctionDef(self, t):

        if t.name == "main":
            self.outputMain(t)
            return


        # Is it a generator ?
        yieldFinder = self.SearchYield(t)
        if yieldFinder.getYield():
            self.generatorWriter.visit(t)
            return


        #for decorator in t.decorator_list:
        #    print(decorator)

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
