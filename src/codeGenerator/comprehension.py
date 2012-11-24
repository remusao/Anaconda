
def visit(self, t):
    self.output.write("from(")
    self.visit(t.target)
    self.output.write(", ")
    self.visit(t.iter)
    self.output.write(")")
    for if_clause in t.ifs:
        self.output.write(" where(")
        self.visit(if_clause)
        self.output.write(")")
