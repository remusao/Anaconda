
def visit(self, t):
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
