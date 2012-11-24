
def visit(self, tree):
    if tree.optional_vars:
        self.output.fill("auto ")
        self.visit(tree.optional_vars)
        self.output.write(" = ")
    self.visit(tree.context_expr)
