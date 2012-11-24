
# TODO : what if lambda doesn't return anything ?
def visit(self, t):
    self.output.write("[&](")
    self.visit(t.args)
    self.output.write(")")

    self.enterScope()
    self.output.fill()
    self.visit(t.body)
    self.leaveScope(None, "")
