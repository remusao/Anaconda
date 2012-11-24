
def visit(self, tree):
    self.visit(tree.name)
    if tree.asname:
        self.output.write(" as %s" % t.asname)
