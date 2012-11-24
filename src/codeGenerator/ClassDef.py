

def visit(self, t):
    self.output.fill()
    self.classWriter.visit(t)


from ast import NodeVisitor


class ClassWriter(NodeVisitor):
    """
    """

    def __init__(self, codeGenerator):
        """
        """
        self.codeGenerator = codeGenerator
        self.className = ""


    def writeConstructors(self, node):
        n = node.name
        # If args
        if len(node.args.args) > 1:
            self.codeGenerator.output.fill("%s() = delete;" % (n))
        else:
            self.codeGenerator.output.fill("%s() = default;" % (n))
        # Copy
        self.codeGenerator.output.fill("%s(const %s&) = default;" % (n, n))
        self.codeGenerator.output.fill("%s& operator=(const %s&) = default;" % (n, n))
        # Move
        self.codeGenerator.output.fill("%s(%s&&) = default;" % (n, n))
        self.codeGenerator.output.fill("%s& operator=(%s&&) = default;" % (n, n))




    def visit(self, node):
        # Constructor
        if node.name == "__init__":
            node.name = self.className
            self.writeConstructors(node)
        else:
            self.codeGenerator.visit(node)



    def visit(self, t):
        self.codeGenerator.output.stackBuffer()
        self.className = t.name
        self.codeGenerator.output.write("\n")

        self.codeGenerator.output.fill("class " + t.name)
        self.codeGenerator.enterScope()
        self.codeGenerator.output.fill("public:")

        #for decorator in t.decorator_list:
        #    print(decorator)

        #for base in t.bases:
        #    print(base)

        #for keyword in t.keywords:
        #    print(keyword)


        for stmt in t.body:
            self.codeGenerator.visit(stmt, self)

        self.codeGenerator.leaveScope(t, "")
        self.codeGenerator.output.write(";")

        self.codeGenerator.output.flushLastInFile(t.name + ".h")
        self.codeGenerator.includes.add(t.name + ".h")
