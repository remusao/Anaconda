#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ast
from classWriter import ClassWriter
from functionWriter import FunctionWriter


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
        self.includes = set([])
        self.output = codeFormatter
        self.classWriter = ClassWriter(self)
        self.functionWriter = FunctionWriter(self)



    def visit_Module(self, tree, extraInfo = None):
        for stmt in tree.body:
            self.visit(stmt)

    # stmt
    def visit_Expr(self, tree, extraInfo = None):
        self.output.fill()
        self.visit(tree.value)


    def visit_Import(self, t, extraInfo = None):
        for name in t.names:
            self.includes.add(name)


    def visit_ImportFrom(self, t, extraInfo = None):
        # A from __future__ import may affect unparsing, so record it.
        if t.module and t.module == '__future__':
            self.future_imports.extend(n.name for n in t.names)

        self.output.fill("from ")
        self.output.write("." * t.level)
        if t.module:
            self.output.write(t.module)
        self.output.write(" import ")
        ##interoutput.leave(lambda: self.output.write(", "), self.visit, t.names)

    def visit_Assign(self, t, extraInfo = None):
        self.output.fill()
        self.output.write("auto ")
        for target in t.targets:
            if extraInfo != None:
                extraInfo.append((target.id, t.value))
            self.visit(target)
            self.output.write(" = ")
        self.visit(t.value)
        self.output.write(";")

    def visit_AugAssign(self, t, extraInfo = None):
        self.output.fill()
        self.visit(t.target)
        self.output.write(" "+self.binop[t.op.__class__.__name__]+"= ")
        self.visit(t.value)

    def visit_Return(self, t, extraInfo = None):
        self.output.fill("return")
        if t.value:
            self.output.write(" ")
            self.visit(t.value)
        self.output.write(";")

    def visit_Pass(self, t, extraInfo = None):
        #self.output.fill("pass")
        pass

    def visit_Break(self, t, extraInfo = None):
        self.output.fill("break")
        self.output.write(";")

    def visit_Continue(self, t, extraInfo = None):
        self.output.fill("continue")
        self.output.write(";")

    # TODO
    def visit_Delete(self, t, extraInfo = None):
        self.output.fill("del ")
        ##interoutput.leave(lambda: self.output.write(", "), self.visit, t.targets)

    # TODO
    def visit_Assert(self, t, extraInfo = None):
        self.output.fill("assert ")
        self.visit(t.test)
        if t.msg:
            self.output.write(", ")
            self.visit(t.msg)

    # TODO
    def visit_Exec(self, t, extraInfo = None):
        self.output.fill("exec ")
        self.visit(t.body)
        if t.globals:
            self.output.write(" in ")
            self.visit(t.globals)
        if t.locals:
            self.output.write(", ")
            self.visit(t.locals)

    # TODO
    def visit_Print(self, t, extraInfo = None):
        self.includes.add("iostream")
        self.output.fill("std::cout ")
        do_comma = True
        for e in t.values:
            if do_comma:self.output.write(" << ")
            else:do_comma=True
            self.visit(e)
        if not t.nl:
            self.output.write(",")
        self.output.write(" << std::endl;")

    def visit_Global(self, t, extraInfo = None):
        #self.output.fill("global ")
        self.output.fill("extern ")
        ##interoutput.leave(lambda: self.output.write(", "), self.output.write, t.names)
        self.output.write(";")

    # TODO
    def visit_Yield(self, t, extraInfo = None):
        self.output.write("(")
        self.output.write("yield")
        if t.value:
            self.output.write(" ")
            self.visit(t.value)
        self.output.write(")")

    # TODO
    def visit_Raise(self, t, extraInfo = None):
        self.output.fill('raise ')
        if t.type:
            self.visit(t.type)
        if t.inst:
            self.output.write(", ")
            self.visit(t.inst)
        if t.tback:
            self.output.write(", ")
            self.visit(t.tback)

    # TODO
    def visit_TryExcept(self, t, extraInfo = None):
        self.output.fill("try")
        self.output.enter()
        self.visit(t.body)
        self.output.leave()

        for ex in t.handlers:
            self.visit(ex)
        if t.orelse:
            self.output.fill("else")
            self.output.enter()
            self.visit(t.orelse)
            self.output.leave()

    # TODO
    def visit_TryFinally(self, t, extraInfo = None):
        if len(t.body) == 1 and isinstance(t.body[0], ast.TryExcept):
            # try-except-finally
            self.visit(t.body)
        else:
            self.output.fill("try")
            self.output.enter()
            self.visit(t.body)
            self.output.leave()

        self.output.fill("finally")
        self.output.enter()
        self.visit(t.finalbody)
        self.output.leave()

    # TODO
    def visit_ExceptHandler(self, t, extraInfo = None):
        self.output.fill("except")
        if t.type:
            self.output.write(" ")
            self.visit(t.type)
        if t.name:
            self.output.write(" as ")
            self.visit(t.name)
        self.output.enter()
        self.visit(t.body)
        self.output.leave()


    def visit_ClassDef(self, t):
        self.classWriter.visit(t)


    def visit_FunctionDef(self, t):
        self.functionWriter.visit(t)


    def visit_For(self, t, extraInfo = None):
        self.output.fill("for (")
        self.visit(t.target)
        self.output.write(" : ")
        self.visit(t.iter)
        self.output.write(")")
        self.output.enter()
        for node in t.body:
            self.visit(node)
        self.output.leave()
        if t.orelse:
            self.output.fill("else")
            self.output.enter()
            self.visit(t.orelse)
            self.output.leave()

    def visit_If(self, t, extraInfo = None):
        self.output.fill("if (")
        self.visit(t.test)
        self.output.enter()
        self.output.write(")")
        for node in t.body:
            self.visit(node)
        self.output.leave()
        # collapse nested ifs into equivalent elifs.
        while (t.orelse and len(t.orelse) == 1 and
               isinstance(t.orelse[0], ast.If)):
            t = t.orelse[0]
            self.output.fill("else if (")
            self.visit(t.test)
            self.output.enter()
            self.visit(t.body)
            self.output.leave()
        # final else
        if t.orelse:
            self.output.fill("else")
            self.output.enter()
            self.visit(t.orelse)
            self.output.leave()

    def visit_While(self, t, extraInfo = None):
        self.output.fill("while (")
        self.visit(t.test)
        setlf.output.write(")")
        self.output.enter()
        self.visit(t.body)
        self.output.leave()
        if t.orelse:
            self.output.fill("else")
            self.output.enter()
            self.visit(t.orelse)
            self.output.leave()

    # TODO
    def visit_With(self, t, extraInfo = None):
        #self.output.fill("with ")
        #self.visit(t.context_expr)
        #if t.optional_vars:
        #    self.output.write(" as ")
        #    self.visit(t.optional_vars)
        #self.output.enter()
        #self.visit(t.body)
        #self.output.leave()
        pass

    # expr
    def visit_Str(self, tree, extraInfo = None):
        # if from __future__ import unicode_literals is in effect,
        # then we want to output string literals using a 'b' prefix
        # and unicode literals with no prefix.
        #if "unicode_literals" not in self.future_imports:
        #    self.output.write(repr(tree.s))
        if isinstance(tree.s, str):
            self.output.write("b" + repr(tree.s))
        elif isinstance(tree.s, unicode):
            self.output.write(repr(tree.s).lstrip("u"))
        else:
            assert False, "shouldn't get here"
        self.output.write(";")

    def visit_Name(self, t, extraInfo = None):
        self.output.write(t.id)

    def visit_Repr(self, t, extraInfo = None):
        self.output.write("`")
        self.visit(t.value)
        self.output.write("`")

    def visit_Num(self, t, extraInfo = None):
        repr_n = repr(t.n)
        # Parenthesize negative numbers, to avoid turning (-1)**2 into -1**2.
        if repr_n.startswith("-"):
            self.output.write("(")
        # Substitute overflowing decimal literal for AST infinities.
        #self.output.write(repr_n.replace("inf", INFSTR))
        if repr_n.startswith("-"):
            self.output.write(")")

    def visit_List(self, t, extraInfo = None):
        self.includes.add("list")
        self.output.write("{")
        ##interoutput.leave(lambda: self.output.write(", "), self.visit, t.elts)
        self.output.write("}")

    # TODO
    def visit_ListComp(self, t, extraInfo = None):
        self.includes.add("list")
        self.output.write("[")
        self.visit(t.elt)
        for gen in t.generators:
            self.visit(gen)
        self.output.write("]")

    # TODO
    def visit_GeneratorExp(self, t, extraInfo = None):
        self.output.write("(")
        self.visit(t.elt)
        for gen in t.generators:
            self.visit(gen)
        self.output.write(")")

    # TODO
    def visit_SetComp(self, t, extraInfo = None):
        self.includes.add("set")
        self.output.write("{")
        self.visit(t.elt)
        for gen in t.generators:
            self.visit(gen)
        self.output.write("}")

    # TODO
    def visit_DictComp(self, t, extraInfo = None):
        self.includes.add("unordered_map")
        self.output.write("{")
        self.visit(t.key)
        self.output.write(": ")
        self.visit(t.value)
        for gen in t.generators:
            self.visit(gen)
        self.output.write("}")

    # TODO
    def visit_comprehension(self, t, extraInfo = None):
        self.output.write(" for ")
        self.visit(t.target)
        self.output.write(" in ")
        self.visit(t.iter)
        for if_clause in t.ifs:
            self.output.write(" if ")
            self.visit(if_clause)

    # TERNARY ? TODO : check
    def visit_IfExp(self, t, extraInfo = None):
        self.output.write("(")
        self.visit(t.test)
        self.output.write(" ? ")
        self.visit(t.body)
        self.output.write(" : ")
        self.visit(t.orelse)
        self.output.write(")")

    # TODO
    def visit_Set(self, t, extraInfo = None):
        assert(t.elts) # should be at least one element
        self.output.write("{")
        #interoutput.leave(lambda: self.output.write(", "), self.visit, t.elts)
        self.output.write("}")

    # TODO
    def visit_Dict(self, t, extraInfo = None):
        self.includes.add("unordered_map")
        self.output.write("{")
        def write_pair(pair):
            (k, v) = pair
            self.output.write("{")
            self.visit(k)
            self.output.write(", ")
            self.visit(v)
            self.output.write("}")
        #interoutput.leave(lambda: self.output.write(", "), output.write_pair, zip(t.keys, t.values))
        self.output.write("}")

    def visit_Tuple(self, t, extraInfo = None):
        self.includes.add("tuple")
        self.output.write("{")
        if len(t.elts) == 1:
            (elt,) = t.elts
            self.visit(elt)
            self.output.write(",")
        else:
            pass
            #interoutput.leave(lambda: self.output.write(", "), self.visit, t.elts)
        self.output.write("}")

    unop = {"Invert":"~", "Not": "not", "UAdd":"+", "USub":"-"}
    def visit_UnaryOp(self, t, extraInfo = None):
        self.output.write("(")
        self.output.write(self.unop[t.op.__class__.__name__])
        self.output.write(" ")
        # If we're applying unary minus to a number, parenthesize the number.
        # This is necessary: -2147483648 is different from -(2147483648) on
        # a 32-bit machine (the first is an int, the second a long), and
        # -7j is different from -(7j).  (The first has real part 0.0, the second
        # has real part -0.0.)
        if isinstance(t.op, ast.USub) and isinstance(t.operand, ast.Num):
            self.output.write("(")
            self.visit(t.operand)
            self.output.write(")")
        else:
            self.visit(t.operand)
        self.output.write(")")

    binop = { "Add":"+", "Sub":"-", "Mult":"*", "Div":"/", "Mod":"%",
                    "LShift":"<<", "RShift":">>", "BitOr":"|", "BitXor":"^", "BitAnd":"&",
                    "FloorDiv":"//", "Pow": "**"}
    def visit_BinOp(self, t, extraInfo = None):
        self.output.write("(")
        self.visit(t.left)
        self.output.write(" " + self.binop[t.op.__class__.__name__] + " ")
        self.visit(t.right)
        self.output.write(")")

    cmpops = {"Eq":"==", "NotEq":"!=", "Lt":"<", "LtE":"<=", "Gt":">", "GtE":">=",
                        "Is":"is", "IsNot":"is not", "In":"in", "NotIn":"not in"}
    def visit_Compare(self, t, extraInfo = None):
        self.output.write("(")
        self.visit(t.left)
        for o, e in zip(t.ops, t.comparators):
            self.output.write(" " + self.cmpops[o.__class__.__name__] + " ")
            self.visit(e)
        self.output.write(")")

    boolops = {ast.And: '&&', ast.Or: '||'}
    def visit_BoolOp(self, t, extraInfo = None):
        self.output.write("(")
        s = " %s " % self.boolops[t.op.__class__]
        #interoutput.leave(lambda: self.output.write(s), self.visit, t.values)
        self.output.write(")")

    def visit_Attribute(self,t, extraInfo = None):
        self.visit(t.value)
        # Special case: 3.__abs__() is a syntax error, so if t.value
        # is an integer literal then we need to either parenthesize
        # it or add an extra space to get 3 .__abs__().
        if isinstance(t.value, ast.Num) and isinstance(t.value.n, int):
            self.output.write(" ")
        self.output.write(".")
        self.output.write(t.attr)

    # TODO
    def visit_Call(self, t, extraInfo = None):
        self.visit(t.func)
        self.output.write("(")
        comma = False
        for e in t.args:
            if comma: self.output.write(", ")
            else: comma = True
            self.visit(e)
        for e in t.keywords:
            if comma: self.output.write(", ")
            else: comma = True
            self.visit(e)
        if t.starargs:
            if comma: self.output.write(", ")
            else: comma = True
            self.output.write("*")
            self.visit(t.starargs)
        if t.kwargs:
            if comma: self.output.write(", ")
            else: comma = True
            self.output.write("**")
            self.visit(t.kwargs)
        self.output.write(")")

    def visit_Subscript(self, t):
        self.visit(t.value)
        self.output.write("[")
        self.visit(t.slice)
        self.output.write("]")

    # TODO
    # slice
    def visit_Ellipsis(self, t, extraInfo = None):
        self.output.write("...")

    def visit_Index(self, t, extraInfo = None):
        self.visit(t.value)

    def visit_Slice(self, t, extraInfo = None):
        if t.lower:
            self.visit(t.lower)
        self.output.write(":")
        if t.upper:
            self.visit(t.upper)
        if t.step:
            self.output.write(":")
            self.visit(t.step)

    # TODO
    def visit_ExtSlice(self, t, extraInfo = None):
        #interoutput.leave(lambda: self.output.write(', '), self.visit, t.dims)
        pass

    # others
    def visit_arguments(self, t, extraInfo = None):
        first = True
        count = 0
        # normal arguments
        defaults = [None] * (len(t.args) - len(t.defaults)) + t.defaults
        for a, d in zip(t.args, defaults):
            if first:
                first = False
            else:
                self.output.write(", ")
            self.output.write("Type%i " % (count))
            self.visit(a)
            count += 1
            if d:
                self.output.write("=")
                self.visit(d)

        # TODO
        # varargs
        if t.vararg:
            if first:first = False
            else: self.output.write(", ")
            self.output.write("*")
            self.output.write(t.vararg)

        # TODO
        # kwargs
        if t.kwarg:
            if first:first = False
            else: self.output.write(", ")
            self.output.write("**"+t.kwarg)

    # TODO
    def visit_keyword(self, t, extraInfo = None):
        self.output.write(t.arg)
        self.output.write("=")
        self.visit(t.value)

    def visit_Lambda(self, t, extraInfo = None):
        self.output.write("[](")
        self.visit(t.args)
        self.output.write(") {")
        self.visit(t.body)
        self.output.write("}")

    # TODO
    def visit_alias(self, t, extraInfo = None):
        self.output.write(t.name)
        if t.asname:
            self.output.write(" as "+t.asname)
