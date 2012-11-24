import ast

def visit(self, t):

    if t.ctx == ast.Store:
        self.variablesInScope[-1].add((t.id, t.ctx))
    toPrint = t.id
    if toPrint == "True":
        toPrint = "true"
    elif toPrint == "False":
        toPrint = "false"

    self.output.write(toPrint)
