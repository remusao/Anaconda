
def visit(self, t):
    self.includes.add("tuple")

    self.output.write("std::make_tuple(")
    self.interLeave(lambda: self.output.write(", "), self.visit, t.elts)
    self.output.write(")")
