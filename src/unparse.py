#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"Usage: unparse.py <path to source file>"
import sys
import ast
import cStringIO
import os

# Large float and imaginary literals get turned into infinities in the AST.
# We unparse those infinities to INFSTR.
INFSTR = "1e" + repr(sys.float_info.max_10_exp + 1)

def interleave(inter, f, seq):
    """
        Call f on each item in seq, calling inter() in between.
    """
    seq = iter(seq)
    try:
        f(next(seq))
    except StopIteration:
        pass
    else:
        for x in seq:
            inter()
            f(x)

### FIND THE RETURN TYPE OF A METHOD


def findTypeOf(assignements, name):
    return "int"

def findReturnType(returnStmt, assignements):


###

class Unparser():
    """
    Methods in this class recursively traverse an AST and
    output source code for the abstract syntax; original formatting
    is disregarded.
    """

    def __init__(self, tree, file = sys.stdout):
        """Unparser(tree, file=sys.stdout) -> None.
         Print the source for tree to file."""
        self.includes = set([])
        self.f = file
        self.future_imports = []
        self._indent = 0
        self.dispatch(tree)
        self.f.write("")
        self.f.flush()

    def fill(self, text = ""):
        "Indent a piece of text, according to the current indentation level"
        self.f.write("\n" + "    " * self._indent + text)

    def write(self, text):
        "Append a piece of text to the current line."
        self.f.write(text)

    def enter(self):
        "Print ':', and increase the indentation."
        self.write("\n{")
        self._indent += 1

    def leave(self):
        "Decrease the indentation level."
        self.write('\n}\n')
        self._indent -= 1

    def dispatch(self, tree, extraInfo = None):
        "Dispatcher function, dispatching tree type T to method _T."
        if isinstance(tree, list):
            for t in tree:
                self.dispatch(t, extraInfo)
            return
        meth = getattr(self, "_" + tree.__class__.__name__)
        meth(tree, extraInfo)


    ############### Unparsing methods ######################
    # There should be one method per concrete grammar type #
    # Constructors should be grouped by sum type. Ideally, #
    # this would follow the order in the grammar, but      #
    # currently doesn't.                                   #
    ########################################################

    def _Module(self, tree, extraInfo = None):
        for stmt in tree.body:
            self.dispatch(stmt)

    # stmt
    def _Expr(self, tree, extraInfo = None):
        self.fill()
        self.dispatch(tree.value)

    def _Import(self, t, extraInfo = None):
        self.fill("import ")
        interleave(lambda: self.write(", "), self.dispatch, t.names)

    def _ImportFrom(self, t, extraInfo = None):
        # A from __future__ import may affect unparsing, so record it.
        if t.module and t.module == '__future__':
            self.future_imports.extend(n.name for n in t.names)

        self.fill("from ")
        self.write("." * t.level)
        if t.module:
            self.write(t.module)
        self.write(" import ")
        interleave(lambda: self.write(", "), self.dispatch, t.names)

    def _Assign(self, t, extraInfo = None):
        self.fill()
        self.write("auto ")
        for target in t.targets:
            if extraInfo != None:
                extraInfo.append((target.id, t.value))
            self.dispatch(target)
            self.write(" = ")
        self.dispatch(t.value)
        self.write(";")

    def _AugAssign(self, t, extraInfo = None):
        self.fill()
        self.dispatch(t.target)
        self.write(" "+self.binop[t.op.__class__.__name__]+"= ")
        self.dispatch(t.value)

    def _Return(self, t, extraInfo = None):
        self.fill("return")
        if t.value:
            self.write(" ")
            self.dispatch(t.value)
        self.write(";")

    def _Pass(self, t, extraInfo = None):
        #self.fill("pass")
        pass

    def _Break(self, t, extraInfo = None):
        self.fill("break")
        self.write(";")

    def _Continue(self, t, extraInfo = None):
        self.fill("continue")
        self.write(";")

    # TODO
    def _Delete(self, t, extraInfo = None):
        self.fill("del ")
        interleave(lambda: self.write(", "), self.dispatch, t.targets)

    # TODO
    def _Assert(self, t, extraInfo = None):
        self.fill("assert ")
        self.dispatch(t.test)
        if t.msg:
            self.write(", ")
            self.dispatch(t.msg)

    # TODO
    def _Exec(self, t, extraInfo = None):
        self.fill("exec ")
        self.dispatch(t.body)
        if t.globals:
            self.write(" in ")
            self.dispatch(t.globals)
        if t.locals:
            self.write(", ")
            self.dispatch(t.locals)

    # TODO
    def _Print(self, t, extraInfo = None):
        self.includes.add("iostream")
        self.fill("std::cout ")
        do_comma = True
        for e in t.values:
            if do_comma:self.write(" << ")
            else:do_comma=True
            self.dispatch(e)
        if not t.nl:
            self.write(",")
        self.write(" << std::endl;")

    def _Global(self, t, extraInfo = None):
        #self.fill("global ")
        self.fill("extern ")
        interleave(lambda: self.write(", "), self.write, t.names)
        self.write(";")

    # TODO
    def _Yield(self, t, extraInfo = None):
        self.write("(")
        self.write("yield")
        if t.value:
            self.write(" ")
            self.dispatch(t.value)
        self.write(")")

    # TODO
    def _Raise(self, t, extraInfo = None):
        self.fill('raise ')
        if t.type:
            self.dispatch(t.type)
        if t.inst:
            self.write(", ")
            self.dispatch(t.inst)
        if t.tback:
            self.write(", ")
            self.dispatch(t.tback)

    # TODO
    def _TryExcept(self, t, extraInfo = None):
        self.fill("try")
        self.enter()
        self.dispatch(t.body)
        self.leave()

        for ex in t.handlers:
            self.dispatch(ex)
        if t.orelse:
            self.fill("else")
            self.enter()
            self.dispatch(t.orelse)
            self.leave()

    # TODO
    def _TryFinally(self, t, extraInfo = None):
        if len(t.body) == 1 and isinstance(t.body[0], ast.TryExcept):
            # try-except-finally
            self.dispatch(t.body)
        else:
            self.fill("try")
            self.enter()
            self.dispatch(t.body)
            self.leave()

        self.fill("finally")
        self.enter()
        self.dispatch(t.finalbody)
        self.leave()

    # TODO
    def _ExceptHandler(self, t, extraInfo = None):
        self.fill("except")
        if t.type:
            self.write(" ")
            self.dispatch(t.type)
        if t.name:
            self.write(" as ")
            self.dispatch(t.name)
        self.enter()
        self.dispatch(t.body)
        self.leave()

    def _ClassDef(self, t, extraInfo = None):
        self.write("\n")
        #for deco in t.decorator_list:
        #    self.fill("@")
        #    self.dispatch(deco)
        self.fill("class " + t.name)
        if t.bases:
            self.write(": ")
            for a in t.bases:
                self.write("public ")
                self.dispatch(a)
                self.write(", ")
            self.write("\n")
        self.enter()
        self.dispatch(t.body)
        self.leave()
        self.write(";")

    # TODO
    def _FunctionDef(self, t, extraInfo = None):
        self.write("\n")
        nbArgs = len(t.args.args)
        if nbArgs > 0:
            self.write("template <")
            for e in xrange(0, nbArgs - 1):
                self.write("typename Type%i" % (e))
                self.write(", ")
            self.write("typename Type%i>" % (nbArgs - 1))
        self.fill("auto " + t.name + "(")
        self.dispatch(t.args)
        self.write(") -> ")

        # Trace the assignements in the function body
        assignements = []

        ### Write body to a temporary buffer

        old_buffer = self.f
        self.f = cStringIO.StringIO()

        self.enter()
        self.dispatch(t.body, assignements)
        self.leave()

        ### Finds the return type
        body = {x.__class__.__name__ : x for x in t.body}
        if "Return" in body:
            old_buffer.write(findReturnType(body["Return"], assignements))
        else:
            old_buffer.write("void")

        old_buffer.write(self.f.getvalue())
        self.f = old_buffer


    def _For(self, t, extraInfo = None):
        self.fill("for (")
        self.dispatch(t.target)
        self.write(" : ")
        self.dispatch(t.iter)
        self.write(")")
        self.enter()
        self.dispatch(t.body)
        self.leave()
        if t.orelse:
            self.fill("else")
            self.enter()
            self.dispatch(t.orelse)
            self.leave()

    def _If(self, t, extraInfo = None):
        self.fill("if (")
        self.dispatch(t.test)
        self.enter()
        self.write(")")
        self.dispatch(t.body)
        self.leave()
        # collapse nested ifs into equivalent elifs.
        while (t.orelse and len(t.orelse) == 1 and
               isinstance(t.orelse[0], ast.If)):
            t = t.orelse[0]
            self.fill("else if (")
            self.dispatch(t.test)
            self.enter()
            self.dispatch(t.body)
            self.leave()
        # final else
        if t.orelse:
            self.fill("else")
            self.enter()
            self.dispatch(t.orelse)
            self.leave()

    def _While(self, t, extraInfo = None):
        self.fill("while (")
        self.dispatch(t.test)
        setlf.write(")")
        self.enter()
        self.dispatch(t.body)
        self.leave()
        if t.orelse:
            self.fill("else")
            self.enter()
            self.dispatch(t.orelse)
            self.leave()

    # TODO
    def _With(self, t, extraInfo = None):
        self.fill("with ")
        self.dispatch(t.context_expr)
        if t.optional_vars:
            self.write(" as ")
            self.dispatch(t.optional_vars)
        self.enter()
        self.dispatch(t.body)
        self.leave()

    # expr
    def _Str(self, tree, extraInfo = None):
        # if from __future__ import unicode_literals is in effect,
        # then we want to output string literals using a 'b' prefix
        # and unicode literals with no prefix.
        if "unicode_literals" not in self.future_imports:
            self.write(repr(tree.s))
        elif isinstance(tree.s, str):
            self.write("b" + repr(tree.s))
        elif isinstance(tree.s, unicode):
            self.write(repr(tree.s).lstrip("u"))
        else:
            assert False, "shouldn't get here"
        self.write(";")

    def _Name(self, t, extraInfo = None):
        self.write(t.id)

    def _Repr(self, t, extraInfo = None):
        self.write("`")
        self.dispatch(t.value)
        self.write("`")

    def _Num(self, t, extraInfo = None):
        repr_n = repr(t.n)
        # Parenthesize negative numbers, to avoid turning (-1)**2 into -1**2.
        if repr_n.startswith("-"):
            self.write("(")
        # Substitute overflowing decimal literal for AST infinities.
        self.write(repr_n.replace("inf", INFSTR))
        if repr_n.startswith("-"):
            self.write(")")

    def _List(self, t, extraInfo = None):
        self.includes.add("list")
        self.write("{")
        interleave(lambda: self.write(", "), self.dispatch, t.elts)
        self.write("}")

    # TODO
    def _ListComp(self, t, extraInfo = None):
        self.includes.add("list")
        self.write("[")
        self.dispatch(t.elt)
        for gen in t.generators:
            self.dispatch(gen)
        self.write("]")

    # TODO
    def _GeneratorExp(self, t, extraInfo = None):
        self.write("(")
        self.dispatch(t.elt)
        for gen in t.generators:
            self.dispatch(gen)
        self.write(")")

    # TODO
    def _SetComp(self, t, extraInfo = None):
        self.includes.add("set")
        self.write("{")
        self.dispatch(t.elt)
        for gen in t.generators:
            self.dispatch(gen)
        self.write("}")

    # TODO
    def _DictComp(self, t, extraInfo = None):
        self.includes.add("unordered_map")
        self.write("{")
        self.dispatch(t.key)
        self.write(": ")
        self.dispatch(t.value)
        for gen in t.generators:
            self.dispatch(gen)
        self.write("}")

    # TODO
    def _comprehension(self, t, extraInfo = None):
        self.write(" for ")
        self.dispatch(t.target)
        self.write(" in ")
        self.dispatch(t.iter)
        for if_clause in t.ifs:
            self.write(" if ")
            self.dispatch(if_clause)

    # TERNARY ? TODO : check
    def _IfExp(self, t, extraInfo = None):
        self.write("(")
        self.dispatch(t.test)
        self.write(" ? ")
        self.dispatch(t.body)
        self.write(" : ")
        self.dispatch(t.orelse)
        self.write(")")

    # TODO
    def _Set(self, t, extraInfo = None):
        assert(t.elts) # should be at least one element
        self.write("{")
        interleave(lambda: self.write(", "), self.dispatch, t.elts)
        self.write("}")

    # TODO
    def _Dict(self, t, extraInfo = None):
        self.includes.add("unordered_map")
        self.write("{")
        def write_pair(pair):
            (k, v) = pair
            self.write("{")
            self.dispatch(k)
            self.write(", ")
            self.dispatch(v)
            self.write("}")
        interleave(lambda: self.write(", "), write_pair, zip(t.keys, t.values))
        self.write("}")

    def _Tuple(self, t, extraInfo = None):
        self.includes.add("tuple")
        self.write("{")
        if len(t.elts) == 1:
            (elt,) = t.elts
            self.dispatch(elt)
            self.write(",")
        else:
            interleave(lambda: self.write(", "), self.dispatch, t.elts)
        self.write("}")

    unop = {"Invert":"~", "Not": "not", "UAdd":"+", "USub":"-"}
    def _UnaryOp(self, t, extraInfo = None):
        self.write("(")
        self.write(self.unop[t.op.__class__.__name__])
        self.write(" ")
        # If we're applying unary minus to a number, parenthesize the number.
        # This is necessary: -2147483648 is different from -(2147483648) on
        # a 32-bit machine (the first is an int, the second a long), and
        # -7j is different from -(7j).  (The first has real part 0.0, the second
        # has real part -0.0.)
        if isinstance(t.op, ast.USub) and isinstance(t.operand, ast.Num):
            self.write("(")
            self.dispatch(t.operand)
            self.write(")")
        else:
            self.dispatch(t.operand)
        self.write(")")

    binop = { "Add":"+", "Sub":"-", "Mult":"*", "Div":"/", "Mod":"%",
                    "LShift":"<<", "RShift":">>", "BitOr":"|", "BitXor":"^", "BitAnd":"&",
                    "FloorDiv":"//", "Pow": "**"}
    def _BinOp(self, t, extraInfo = None):
        self.write("(")
        self.dispatch(t.left)
        self.write(" " + self.binop[t.op.__class__.__name__] + " ")
        self.dispatch(t.right)
        self.write(")")

    cmpops = {"Eq":"==", "NotEq":"!=", "Lt":"<", "LtE":"<=", "Gt":">", "GtE":">=",
                        "Is":"is", "IsNot":"is not", "In":"in", "NotIn":"not in"}
    def _Compare(self, t, extraInfo = None):
        self.write("(")
        self.dispatch(t.left)
        for o, e in zip(t.ops, t.comparators):
            self.write(" " + self.cmpops[o.__class__.__name__] + " ")
            self.dispatch(e)
        self.write(")")

    boolops = {ast.And: '&&', ast.Or: '||'}
    def _BoolOp(self, t, extraInfo = None):
        self.write("(")
        s = " %s " % self.boolops[t.op.__class__]
        interleave(lambda: self.write(s), self.dispatch, t.values)
        self.write(")")

    def _Attribute(self,t, extraInfo = None):
        self.dispatch(t.value)
        # Special case: 3.__abs__() is a syntax error, so if t.value
        # is an integer literal then we need to either parenthesize
        # it or add an extra space to get 3 .__abs__().
        if isinstance(t.value, ast.Num) and isinstance(t.value.n, int):
            self.write(" ")
        self.write(".")
        self.write(t.attr)

    # TODO
    def _Call(self, t, extraInfo = None):
        self.dispatch(t.func)
        self.write("(")
        comma = False
        for e in t.args:
            if comma: self.write(", ")
            else: comma = True
            self.dispatch(e)
        for e in t.keywords:
            if comma: self.write(", ")
            else: comma = True
            self.dispatch(e)
        if t.starargs:
            if comma: self.write(", ")
            else: comma = True
            self.write("*")
            self.dispatch(t.starargs)
        if t.kwargs:
            if comma: self.write(", ")
            else: comma = True
            self.write("**")
            self.dispatch(t.kwargs)
        self.write(")")

    def _Subscript(self, t):
        self.dispatch(t.value)
        self.write("[")
        self.dispatch(t.slice)
        self.write("]")

    # TODO
    # slice
    def _Ellipsis(self, t, extraInfo = None):
        self.write("...")

    def _Index(self, t, extraInfo = None):
        self.dispatch(t.value)

    def _Slice(self, t, extraInfo = None):
        if t.lower:
            self.dispatch(t.lower)
        self.write(":")
        if t.upper:
            self.dispatch(t.upper)
        if t.step:
            self.write(":")
            self.dispatch(t.step)

    # TODO
    def _ExtSlice(self, t, extraInfo = None):
        interleave(lambda: self.write(', '), self.dispatch, t.dims)

    # others
    def _arguments(self, t, extraInfo = None):
        first = True
        count = 0
        # normal arguments
        defaults = [None] * (len(t.args) - len(t.defaults)) + t.defaults
        for a, d in zip(t.args, defaults):
            if first:
                first = False
            else:
                self.write(", ")
            self.write("Type%i " % (count))
            self.dispatch(a)
            count += 1
            if d:
                self.write("=")
                self.dispatch(d)

        # TODO
        # varargs
        if t.vararg:
            if first:first = False
            else: self.write(", ")
            self.write("*")
            self.write(t.vararg)

        # TODO
        # kwargs
        if t.kwarg:
            if first:first = False
            else: self.write(", ")
            self.write("**"+t.kwarg)

    # TODO
    def _keyword(self, t, extraInfo = None):
        self.write(t.arg)
        self.write("=")
        self.dispatch(t.value)

    def _Lambda(self, t, extraInfo = None):
        self.write("[](")
        self.dispatch(t.args)
        self.write(") {")
        self.dispatch(t.body)
        self.write("}")

    # TODO
    def _alias(self, t, extraInfo = None):
        self.write(t.name)
        if t.asname:
            self.write(" as "+t.asname)
