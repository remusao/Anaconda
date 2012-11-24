
# TODO
def visit(self, t):
    self.output.write("catch (")
    if not (t.type and t.name):
        self.output.write("...)")
    else:
        self.output.write(" ")
        self.visit(t.type)
        self.output.write(" ")
        self.visit(t.name)
        self.output.write(")")
    self.enterScope()
    self.visit(t.body)
    self.leaveScope()
