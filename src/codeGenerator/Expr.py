
def visit(self, tree):
    self.output.fill()
    self.visit(tree.value)
    self.output.write(";")
