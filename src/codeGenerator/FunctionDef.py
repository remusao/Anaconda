
from ast import NodeVisitor, Name
from treeUtils import *


def visit(self, t):
    """ Visit the FunctionDef according to its kind """
    self.fill

    if isGenerator(self, t):
        visitGenerator(self, t)
    else:
        visitNormal(self, t)



def isGenerator(self, tree):
    return NodeFinder().findFirst(tree, ['Yield'])


def visitGenerator(self, tree):
    self.write('// Generator')

    name = t.name
    # Type of the Generator
    type = findType(self.variablesInScope[-1], NodeFinder().findAll(t, ['Return']), tree)

    # include directives
    self.includes.add("generator.h")
    self.includes.add("coroutine.h")
    self.includes.add("yield.h")


    self.fill()
    nbArgs = len(t.args.args)
    if nbArgs > 0:
        self.write("template <")
        for e in range(0, nbArgs - 1):
            self.write("typename Type%i" % (e))
            self.write(", ")
        self.write("typename Type%i>" % (nbArgs - 1))
    self.fill("auto " + t.name + "(")
    self.visit(t.args)
    self.write(") -> ")

    ### write body to a temporary buffer

    self.output.stackBuffer()
    self.enterScope()


    self.fill("coroutine c;")
    self.fill("return Generator<long int>([=]() mutable -> long int")

    self.enterScope()
    self.fill("reenter(c)")
    self.enterScope()
    self.visit(t.body)

    self.leaveScope(None, "")
    self.fill("throw EndOfGenerator();")
    self.leaveScope(None, ");")
    self.leaveScope(t)

    tmpBuffer = self.output.topPop()

    ### Finds the return type
    self.write("Generator<")
    self.write(">")

    self.write(tmpBuffer.getvalue())



def visitNormal(self, t):

    #for decorator in t.decorator_list:
    #    print(decorator)

    self.fill()
    nbArgs = len(t.args.args)
    if nbArgs > 0:
        self.write("template <")
        for e in range(0, nbArgs - 1):
            self.write("typename Type%i" % (e))
            self.write(", ")
        self.write("typename Type%i>" % (nbArgs - 1))
    self.fill("auto " + t.name + "(")
    self.visit(t.args)
    self.write(") -> ")

    ### write body to a temporary buffer

    self.output.stackBuffer()
    self.enterScope()

    self.visit(t.body)

    self.leaveScope(t)

    tmpBuffer = self.output.topPop()

    ### Finds the return type
    self.write('decltype(')
    type = findType(self.variablesInScope[-1], NodeFinder().findAll(t, ['Return']), t)

    if type:
        self.visit(type)
    else:
        self.write('void')
    self.write(')')

    self.write(tmpBuffer.getvalue())



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
            res = allInScope(minReturn, scope)
            if len(res) == 0:
                break
            for name in res:
                definition = getDefinition(tree, name.id)
                minReturn = replacer(name.id, definition, minReturn)
        return minReturn
