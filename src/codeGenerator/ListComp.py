
def visit(self, t):
    self.includes.add("vector")
    self.includes.add("linq.h")
    self.output.write("LINQ(")
    self.visit(t.generators)
    self.output.write(" select(")
    self.visit(t.elt)
    self.output.write("))")
