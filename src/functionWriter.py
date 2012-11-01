#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ast import NodeVisitor, Name


class FunctionWriter(NodeVisitor):
    """
    """

    def __init__(self, codeGenerator):
        """ """
        self.codeGenerator = codeGenerator


    def generic_visit(self, node):
        """  """
        self.codeGenerator.visit(node)


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



    class SearchReturn(NodeVisitor):

        def __init__(self, node):
            self.ret = None
            self.visit(node)

        def visit_Return(self, node):
            self.ret = node

        def getReturn(self):
            return self.ret


    def visit_arguments(self, t):
        first = True
        count = 0
        # normal arguments
        defaults = [None] * (len(t.args) - len(t.defaults)) + t.defaults
        for a, d in zip(t.args, defaults):
            if first:
                first = False
            else:
                self.codeGenerator.output.write(", ")
            self.codeGenerator.output.write("Type%i " % (count))
            self.visit(a)
            count += 1
            if d:
                self.codeGenerator.output.write("=")
                self.visit(d)

        # TODO
        # varargs
        if t.vararg:
            if first:first = False
            else: self.codeGenerator.output.write(", ")
            self.codeGenerator.output.write("*")
            self.codeGenerator.output.write(t.vararg)

        # TODO
        # kwargs
        if t.kwarg:
            if first:first = False
            else: self.codeGenerator.output.write(", ")
            self.codeGenerator.output.write("**"+t.kwarg)


    # TODO
    def visit_FunctionDef(self, t):

        #for decorator in t.decorator_list:
        #    print(decorator)

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
        self.codeGenerator.output.enter()

        self.visit(t.body)

        self.codeGenerator.output.leave()

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
