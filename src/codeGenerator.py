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
        self.scope = 0
        self.variablesInScope = [set([])]
        self.includes = set([])
        self.output = codeFormatter
        self.classWriter = ClassWriter(self)
        self.functionWriter = FunctionWriter(self)


    def visit(self, node, target = None):
        if not target:
            target = self
        if isinstance(node, list):
            for n in node:
                if self.scopeOpener(n):
                    self.visit(n, target)
        else:
            # Try to find the method in target. If the method doesn't exist, we
            # try to find the method in CodeGenerator.
            if self.scopeOpener(node):
                getattr(target, "visit_%s" % (node.__class__.__name__), self.visit)(node)


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
    unaryop = {
        "Invert" : "~",
        "Not" : "!",
        "UAdd" : "+",
        "USub" : "-"
    }
    binop = {
        "Add" : "+",
        "Sub" : "-",
        "Mult" : "*",
        "Div" : "/",
        "Mod" : "%",
        "LShift" : "<<",
        "RShift" : ">>",
        "BitOr" : "|",
        "BitXor" : "^",
        "BitAnd" : "&",
        "FloorDiv" : "//",
        "Pow" : "**"
    }
    boolop = {
        ast.And : '&&',
        ast.Or : '||'
    }
    cmpops = {
        "Eq" : "==",
        "NotEq" : "!=",
        "Lt" : "<",
        "LtE" : "<=",
        "Gt" : ">",
        "GtE" : ">=",
        "Is" : "==",
        "IsNot" : "!=",
        "In" : "in",
        "NotIn" : "not in"
    }


    #           #
    #    MOD    #
    #           #


    def visit_Module(self, tree):
        self.visit(tree.body)


    def visit_Interactive(self, tree):
        self.visit(tree.body)


    def visit_Expression(self, tree):
        self.visit(tree.body)


    def visit_Suite(self, tree):
        self.visit(tree.body)


    #            #
    #    STMT    #
    #            #


    def visit_FunctionDef(self, t):
        self.output.fill()
        self.functionWriter.visit(t)


    def visit_ClassDef(self, t):
        self.output.fill()
        self.classWriter.visit(t)


    def visit_Return(self, t):
        self.output.fill("return")
        if t.value:
            self.output.write(" ")
            self.visit(t.value)
        self.output.write(";")


    def visit_Delete(self, t):
        self.output.fill("delete ")
        self.interLeave((lambda: self.output.write(", ")), self.visit, t.targets)
        self.output.write(";")


    def visit_Assign(self, t):
        for target in t.targets:
            self.output.fill()
            if isinstance(target, ast.Name):
                if target.id not in self.variablesInScope[-1]:
                    self.variablesInScope[-1].add(target.id)
                    self.output.write("auto ")
            self.visit(target)
            self.output.write(" = ")
            self.visit(t.value)
            self.output.write(";")


    def visit_AugAssign(self, t):
        self.output.fill()
        self.visit(t.target)
        self.output.write(" %s= " % (self.binop[t.op.__class__.__name__]))
        self.visit(t.value)
        self.output.write(";")


    def visit_For(self, t):
        self.output.fill("for (auto ")
        self.visit(t.target)
        self.output.write(" : ")
        self.visit(t.iter)
        self.output.write(")")
        self.enterScope()
        self.visit(t.body)
        self.leaveScope()
        #if t.orelse:
        #    self.output.fill("else")
        #    self.enterScope()
        #    self.visit(t.orelse)
        #    self.leaveScope()


    def visit_While(self, t):
        self.output.fill("while (")
        self.visit(t.test)
        self.output.write(")")

        self.enterScope()
        self.visit(t.body)
        self.leaveScope()

        #if t.orelse:
        #    self.output.fill("else")
        #    self.enterScope()
        #    self.visit(t.orelse)
        #    self.leaveScope()


    def visit_If(self, t):
        self.output.fill("if (")
        self.visit(t.test)
        self.output.write(")")

        self.enterScope()
        self.visit(t.body)
        self.leaveScope()

        # TODO
        # collapse nested ifs into equivalent elifs.
        while (t.orelse and len(t.orelse) == 1 and
               isinstance(t.orelse[0], ast.If)):
            t = t.orelse[0]
            self.output.fill("else if (")
            self.visit(t.test)
            self.output.write(")")
            self.enterScope()
            self.visit(t.body)
            self.leaveScope()
            del t.orelse[0]
        # final else
        if t.orelse:
            self.output.fill("else")
            self.enterScope()
            self.visit(t.orelse[0])
            self.leaveScope()


    # TODO
    def visit_With(self, t):
        self.output.fill("/// With ")
        #self.visit(t.context_expr)
        #if t.optional_vars:
        #    self.output.write("auto ")
        #    self.visit(t.optional_vars)
        #    self.output.write(" = ")
        #self.visit(t.context_expr)

        self.enterScope()
        self.visit(t.items)
        self.visit(t.body)
        self.leaveScope(None, "")

        pass


    def visit_Raise(self, t):
        if t.exc:
            self.output.fill('throw ' + t.exc)


    def visit_Try(self, t):
        self.output.fill("try")

        self.enterScope()
        self.visit(t.body)
        self.leaveScope()

        self.visit(t.handlers)


    def visit_Assert(self, t):
        self.includes.add("cassert")
        self.output.fill("assert(")
        self.visit(t.test)
        #if t.msg:
        #    self.output.write(", ")
        #    self.visit(t.msg)
        self.output.write(");")


    # TODO : check if it's standard lib or a file in the project
    def visit_Import(self, t):
        for name in t.names:
            self.includes.add(name.name)


    # TODO : check if it's standard lib or a file in the project
    def visit_ImportFrom(self, t):
        module = '/'
        if t.module:
            module += t.module
        self.includes.add("%s%s" % ('.' * t.level, t.module))
        #for name in t.names:
        #    self.includes.add("%s%s/%s" % ('.' * t.level, t.module, name.name))


    def visit_Global(self, t):
        self.output.fill("extern ")
        self.interLeave(lambda: self.output.write(", "), self.visit, t.names)
        self.output.write(";")


    # TODO
    def visit_Nonlocal(self, tree):
        self.output.fill()
        self.visit(tree.names)


    def visit_Expr(self, tree):
        self.output.fill()
        self.visit(tree.value)
        self.output.write(";")


    def visit_Pass(self, t):
        self.output.fill(";")


    def visit_Break(self, t):
        self.output.fill("break;")


    def visit_Continue(self, t):
        self.output.fill("continue;")


    def visit_attributes(self, tree):
        pass


    #            #
    #    EXPR    #
    #            #


    def visit_BoolOp(self, t):
        s = " %s " % self.boolop[t.op.__class__]
        self.interLeave(lambda: self.output.write(s), self.visit, t.values)


    def visit_BinOp(self, t):
        self.visit(t.left)
        self.output.write(" %s " % (self.binop[t.op.__class__.__name__]))
        self.visit(t.right)


    def visit_UnaryOp(self, t):
        parenthesize = isinstance(t.op, ast.USub) and isinstance(t.operand, ast.Num)
        if parenthesize:
            self.output.write("(")
        self.output.write(self.unaryop[t.op.__class__.__name__])
        self.visit(t.operand)
        if parenthesize:
            self.output.write(")")


    # TODO : what if lambda doesn't return anything ?
    def visit_Lambda(self, t):
        self.output.write("[&](")
        self.visit(t.args)
        self.output.write(")")

        self.enterScope()
        self.output.fill()
        self.visit(t.body)
        self.leaveScope(None, "")


    def visit_IfExp(self, t):
        self.output.write("(")
        self.visit(t.test)
        self.output.write(" ? ")
        self.visit(t.body)
        self.output.write(" : ")
        self.visit(t.orelse)
        self.output.write(")")


    # TODO : Handle empty dic
    def visit_Dict(self, t):
        self.includes.add("unordered_map")

        # Find type of the keys
        self.output.stackBuffer()
        self.visit(t.values[0])
        type1 = self.output.topPop().getvalue()

        # Find type of the values
        self.output.stackBuffer()
        self.visit(t.keys[0])
        type2 = self.output.topPop().getvalue()

        # declare the type
        self.output.write("std::unordered_map<decltype (%s), decltype (%s)>"
                         % (type1, type2))
        self.enterScope()
        def write_pair(pair):
            (k, v) = pair
            self.output.fill()
            self.output.write("{")
            self.visit(k)
            self.output.write(", ")
            self.visit(v)
            self.output.write("}")
        self.interLeave(lambda: self.output.write(", "), write_pair,
                        list(zip(t.keys, t.values)))
        self.leaveScope(None, "")


    def visit_Set(self, t):
        self.includes.add("set")
        assert(t.elts) # should be at least one element

        # Find type of the keys
        self.output.stackBuffer()
        self.visit(t.elts[0])
        type = self.output.topPop().getvalue()

        self.output.write("std::set<decltype (%s)>" % (type))
        self.enterScope()
        self.output.fill()
        self.interLeave(lambda: self.output.write(", "), self.visit, t.elts)
        self.leaveScope(None, "")


    def visit_ListComp(self, t):
        self.includes.add("vector")
        self.includes.add("linq.h")
        self.output.write("LINQ(")
        self.visit(t.generators)
        self.output.write(" select(")
        self.visit(t.elt)
        self.output.write("))")


    # TODO
    def visit_SetComp(self, t):
        self.includes.add("set")
        self.output.write("{")
        self.visit(t.elt)
        self.visit(t.generators)
        self.output.write("}")


    # TODO
    def visit_DictComp(self, t):
        self.includes.add("unordered_map")
        self.output.write("{")
        self.visit(t.key)
        self.output.write(": ")
        self.visit(t.value)
        self.visit(t.generators)
        self.output.write("}")


    # TODO : use coroutine
    def visit_GeneratorExp(self, t):
        self.output.write("(")
        self.visit(t.elt)
        self.visit(t.generators)
        self.output.write(")")


    # TODO : use coroutine
    def visit_Yield(self, t):
        pass
        #self.output.write("(")
        #self.output.write("yield")
        #if t.value:
        #    self.output.write(" ")
        #    self.visit(t.value)
        #self.output.write(")")


    # TODO : use coroutine
    def visit_YieldFrom(self, tree):
        self.visit(tree.value)


    def visit_Compare(self, t):
        self.visit(t.left)
        for o, e in zip(t.ops, t.comparators):
            self.output.write(" %s " % (self.cmpops[o.__class__.__name__]))
            self.visit(e)


    # TODO
    def visit_Call(self, t):
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


    def visit_Num(self, t):
        repr_n = repr(t.n)
        # Parenthesize negative numbers, to avoid turning (-1)**2 into -1**2.
        if repr_n.startswith("-"):
            self.output.write("(")
        self.output.write(str(t.n))
        # Substitute overflowing decimal literal for AST infinities.
        #self.output.write(repr_n.replace("inf", INFSTR))
        if repr_n.startswith("-"):
            self.output.write(")")


    def visit_Str(self, tree):
        if isinstance(tree.s, str):
            self.output.write('"%s"' % (tree.s))
        elif isinstance(tree.s, unicode):
            self.output.write(repr(tree.s).lstrip("u"))
        else:
            assert False, "shouldn't get here"


    def visit_Bytes(self, tree):
        # tree.s
        self.output.write(tree.s)


    # TODO
    # slice
    def visit_Ellipsis(self, t):
        self.output.write("...")


    #############
    #  Assignment Context
    #############


    def visit_Attribute(self, t):
        self.visit(t.value)
        # Special case: 3.__abs__() is a syntax error, so if t.value
        # is an integer literal then we need to either parenthesize
        # it or add an extra space to get 3 .__abs__().
        if isinstance(t.value, ast.Num) and isinstance(t.value.n, int):
            self.output.write(" ")
        self.output.write(".")
        self.output.write(t.attr)


    def visit_Subscript(self, t):
        self.visit(t.value)
        self.output.write("[")
        self.visit(t.slice)
        self.output.write("]")


    def visit_Starred(self, tree):
        self.visit(tree.value)


    def visit_Name(self, t):
        toPrint = t.id
        if toPrint == "True":
            toPrint = "true"
        elif toPrint == "False":
            toPrint = "false"

        self.output.write(toPrint)


    def visit_List(self, t):
        self.includes.add("vector")

        # Find type of the elements
        self.output.stackBuffer()
        self.visit(t.elts[0])
        type = self.output.topPop().getvalue()

        self.output.write("std::vector<decltype (%s)>" % (type))
        self.enterScope()
        self.output.fill()
        self.interLeave(lambda: self.output.write(", "), self.visit, t.elts)
        self.leaveScope(None, "")


    def visit_Tuple(self, t):
        self.includes.add("tuple")

        self.output.write("std::make_tuple(")
        self.interLeave(lambda: self.output.write(", "), self.visit, t.elts)
        self.output.write(")")


    # TODO
    def visit_Slice(self, t):
        if t.lower:
            self.visit(t.lower)
        self.output.write(":")
        if t.upper:
            self.visit(t.upper)
        if t.step:
            self.output.write(":")
            self.visit(t.step)


    # TODO
    def visit_ExtSlice(self, t):
        #interoutput.leave(lambda: self.output.write(', '), self.visit, t.dims)
        pass


    # TODO
    def visit_Index(self, t):
        self.visit(t.value)


    # TODO
    def visit_ExceptHandler(self, t):
        self.output.write("catch (")
        if not (t.type and t.name):
            self.output.write("...)")
        else:
            self.output.write(" ")
            self.visit(t.type)
            self.output.write(" ")
            self.visit(t.name)
            self.output.write(")")
        self.enterScope()
        self.visit(t.body)
        self.leaveScope()


    def visit_comprehension(self, t):
        self.output.write("from(")
        self.visit(t.target)
        self.output.write(", ")
        self.visit(t.iter)
        self.output.write(")")
        for if_clause in t.ifs:
            self.output.write(" where(")
            self.visit(if_clause)
            self.output.write(")")


    # TODO
    def visit_arguments(self, t):
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
            self.variablesInScope[-1].add(a.arg)
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




    def visit_arg(self, tree):
        self.output.write(tree.arg)


    def visit_keyword(self, tree):
        self.visit(tree.arg)
        self.output.write("=")
        self.visit(tree.value)


    def visit_alias(self, tree):
        self.visit(tree.name)
        if tree.asname:
            self.output.write(" as %s" % t.asname)


    def visit_withitem(self, tree):
        if tree.optional_vars:
            self.output.fill("auto ")
            self.visit(tree.optional_vars)
            self.output.write(" = ")
        self.visit(tree.context_expr)
