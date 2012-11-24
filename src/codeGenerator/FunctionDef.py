
from ast import NodeVisitor, Name
from nodeFinder import NodeFinder


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
    type = findType(NodeFinder().findAll(t, ['Return']))

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
    self.write(findType(NodeFinder().findAll(t, ['Return'])))
    self.write(tmpBuffer.getvalue())


def findType(returns):
    return 'int'
