
def visit(self, t):
    self.output.fill("extern ")
    self.interLeave(lambda: self.output.write(", "), self.visit, t.names)
    self.output.write(";")
