
from ast import NodeVisitor, Name
from treeUtils import *


def visit(self, t):
    """ Visit the FunctionDef according to its kind """
    self.variablesInScope[-1].add(t.name)

    if isGenerator(self, t):
        visitGenerator(self, t)
    else:
        visitNormal(self, t)



def isGenerator(self, tree):
    return NodeFinder().findFirst(tree, ['Yield'])


def visitGenerator(self, t):

    name = t.name               # name of the generator
    fname = name + "Functor"    # name of the functor



    # include directives
    self.includes.add("generator.h")
    self.includes.add("coroutine.h")
    self.includes.add("yield.h")


    self.write('\n')

    args = []
    nbArgs = len(t.args.args)
    if nbArgs > 0:
        self.write("template <")
        for e in range(0, nbArgs - 1):
            args.append(t.args.args[e].arg)
            self.write("typename T%i" % (e))
            self.write(", ")
        args.append(t.args.args[nbArgs - 1].arg)
        self.write("typename T%i>" % (nbArgs - 1))
    self.fill("auto " + t.name + "(")
    self.visit(t.args)

    # Type of the Generator
    type = findType(self.variablesInScope[-1], NodeFinder().findAll(t, ['Yield']), t)
    type = ('decltype(%s)' % (self.getStr(type))) if type else 'void'
    genType = "__Generator<%s>" % type

    self.write(") -> " + genType)

    ### write body to a temporary buffer

    self.enterScope()

    self.fill("struct " + fname)
    self.enterScope()

    for i, j in enumerate(args):
        self.fill("T%s %s;" % (i, j))
    self.fill("coroutine __coroutine;")
    # Search all the local variables in the functor to
    # forward-declare them
    # TODO

    self.write('\n')

    # Delete constructors and operator=
    self.fill("%s() = delete;" % (fname))
    # TODO : Find a solution to avoid using copy constructor with std::function
    self.fill("%s(const %s&) = default;" % (fname, fname))
    self.fill("%s& operator=(const %s&) = delete;" % (fname, fname))
    self.write('\n')

    # Declare the constructor
    self.fill("%s(%s&&) = default;" % (fname, fname))
    self.fill("%s& operator=(%s&&) = default;" % (fname, fname))

    self.fill("%s(" % fname)
    if len(args) > 0:
        self.write("const T%s %s" % (0, args[0]))
        for i, j in enumerate(args[1:]):
            self.write(", const T%s %s" % (i, j))
    self.write(")")
    self.enterScope()
    for arg in args:
        self.fill("this->%s = %s;" % (arg, arg))
    self.leaveScope(None, "")

    self.write('\n')
    self.fill("%s operator()()" % type)
    self.enterScope()
    self.fill("reenter(this->__coroutine)")
    self.enterScope()
    self.visit(t.body)
    self.leaveScope(None, "")
    self.fill("throw __EndOfGenerator();")
    self.leaveScope(None, "")
    self.leaveScope(None, ";")

    self.fill("return __Generator<%s>(%s(%s));" % (type, fname, ', '.join(args)))
    self.leaveScope()



def visitNormal(self, t):

    #for decorator in t.decorator_list:
    #    print(decorator)


    #if type:
    #    type = self.getStr(type)
    #else:
    #    type = 'void'


    self.write('\n')
    nbArgs = len(t.args.args)
    if nbArgs > 0:
        self.write("template <")
        for e in range(0, nbArgs - 1):
            self.write("typename T%i" % (e))
            self.write(", ")
        self.write("typename T%i>" % (nbArgs - 1))
    self.fill("auto " + t.name + "(")
    self.visit(t.args)

    ### Finds the return type
    type = findType(self.variablesInScope[-1], NodeFinder().findAll(t, ['Return']), t)
    type = ('decltype(%s)' % self.getStr(type)) if type else 'void'

    self.write(") -> %s" % type)

    # Output body
    self.enterScope()
    self.visit(t.body)
    self.leaveScope(t)




def findType(scope, returns, tree):

    if len(returns) == 0:
        return None

    def getMin(l):
        """ Return the Tree of minimal size """
        if l:
            minReturn, minSize = l[0]
            for r, s in l:
                if s < minSize:
                    minSize = s
                    minReturn = r
            return r
        return None

    size = TreeSize()
    allInScope = AllInScope()

    l = [(r.value, size(r.value)) for r in returns]
    # Try to find a return statement which use identifiers in the scope
    okReturns = [(r, s) for (r, s) in l if len(allInScope(r, scope)) == 0]
    # We return the smallest
    if len(okReturns) != 0:
        return getMin(okReturns)
    else:
        # Take the smallest tree and try to replace the node not in the
        # scope by their definition
        minReturn = getMin(l)
        replacer = ReplaceNode()
        getDefinition = GetDefinition()
        while True:
            res = [x for x in allInScope(minReturn, scope) if isinstance(x, ast.Name)]
            if len(res) == 0:
                break
            for name in res:
                definition = getDefinition(tree, name.id)
                minReturn = replacer(name.id, definition, minReturn)
        return minReturn
