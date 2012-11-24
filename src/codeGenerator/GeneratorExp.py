
# TODO : use coroutine
def visit(self, t):
    self.output.write("(")
    self.visit(t.elt)
    self.visit(t.generators)
    self.output.write(")")
