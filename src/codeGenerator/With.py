
# TODO
def visit(self, t):
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
