
def visit(self, t):
    self.output.fill("try")

    self.enterScope()
    self.visit(t.body)
    self.leaveScope()

    self.visit(t.handlers)
