import ast

def visit(self, t):

    if t.ctx == ast.Store:
        self.variablesInScope[-1].add((t.id, t.ctx))
    self.output.write(t.id)
