#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import sys

class CodeGenerator(ast.NodeVisitor):
    """
        Methods in this class recursively traverse an AST and
        output source code for the abstract syntax; original formatting
        is disregarded.
    """

    def __init__(self, codeFormatter):
        """
            Unparser(tree, file=sys.stdout) -> None.
            Print the source for tree to file.
        """
        sys.path.append("codeGenerator")
        self.scope = 0
        self.variablesInScope = [set([])]
        self.includes = set([])
        self.output = codeFormatter
        self.visitors = {}


    def visit(self, node):
        if isinstance(node, list):
            for n in node:
                if self.scopeOpener(n):
                    self.visit(n)
        else:
            # Try to find the method in target. If the method doesn't exist, we
            # try to find the method in CodeGenerator.
            if self.scopeOpener(node):
                if node.__class__.__name__ in self.visitors:
                    self.visitor[node.__class__.__name__](node)
                else:
                    module = __import__(node.__class__.__name__)
                    module.visit(self, node)
                    #getattr(, "visit_%s" % (node.__class__.__name__), self.visit)(node)


    def printIncludes(self):
        self.output.stackBuffer()
        for include in self.includes:
            self.output.write("#include ")
            if include.find(".h") != -1:
                self.output.write("\"%s\"\n" % (include))
            else:
                self.output.write("<%s>\n" % (include))

        tmp = self.output.topPop()
        tmp.write(self.output.topPop().getvalue())
        self.output.pushBuffer(tmp)


    def interLeave(self, output, visit, l):
        if len(l) > 1:
            visit(l[0])
            for val in l[1:]:
                output()
                visit(val)
        elif len(l):
            visit(l[0])


    def scopeOpener(self, node):
        """
        Makes sure that nothing could be written outside of any class
        or function. (indentation at 0)
        """
        if self.scope > 0:
            return True
        else:
            if node.__class__.__name__ in ["Module", "ClassDef", "FunctionDef"]:
                self.scope += 1
                return True
        return False


    def fill(self, text = ""):
        self.output.fill(text)


    def write(self, text):
        self.output.write(text)


    def enterScope(self):
        self.output.enter()
        self.variablesInScope.append(set(self.variablesInScope[-1]))


    def leaveScope(self, node = None, suffix = "\n"):
        self.output.leave(suffix)
        if node and node.__class__.__name__ in ["Module", "ClassDef", "FunctionDef"]:
            self.scope -= 1
        del self.variablesInScope[-1]


    #
    # Dict
    #
    expr_context = {
        "Load" : "",
        "Store" : "",
        "Del" : "",
        "AugLoad" : "",
        "AugStore" : "",
        "Param" : ""
    }
