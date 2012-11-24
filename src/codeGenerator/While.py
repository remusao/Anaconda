
def visit(self, t):
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
