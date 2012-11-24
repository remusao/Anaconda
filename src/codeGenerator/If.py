
def visit(self, t):
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
