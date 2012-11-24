
def visit(self, t):
    self.output.fill("return")
    if t.value:
        self.output.write(" ")
        self.visit(t.value)
    self.output.write(";")
