
def visit(self, tree):
    self.visit(tree.arg)
    self.output.write("=")
    self.visit(tree.value)
