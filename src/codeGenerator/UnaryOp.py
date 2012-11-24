import ast

unaryop = {
    "Invert" : "~",
    "Not" : "!",
    "UAdd" : "+",
    "USub" : "-"
}


def visit(self, t):
    parenthesize = isinstance(t.op, ast.USub) and isinstance(t.operand, ast.Num)
    if parenthesize:
        self.output.write("(")
    self.output.write(unaryop[t.op.__class__.__name__])
    self.visit(t.operand)
    if parenthesize:
        self.output.write(")")
