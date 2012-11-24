
def visit(self, t):
    self.visit(t.value)
    self.output.write("[")
    self.visit(t.slice)
    self.output.write("]")
