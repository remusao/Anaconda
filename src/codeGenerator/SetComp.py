
# TODO
def visit(self, t):
    self.includes.add("set")
    self.output.write("{")
    self.visit(t.elt)
    self.visit(t.generators)
    self.output.write("}")
