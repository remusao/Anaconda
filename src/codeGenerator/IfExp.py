
def visit(self, t):
    self.output.write("(")
    self.visit(t.test)
    self.output.write(" ? ")
    self.visit(t.body)
    self.output.write(" : ")
    self.visit(t.orelse)
    self.output.write(")")
