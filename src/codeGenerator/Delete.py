
def visit(self, t):
    self.output.fill("delete ")
    self.interLeave((lambda: self.output.write(", ")), self.visit, t.targets)
    self.output.write(";")
