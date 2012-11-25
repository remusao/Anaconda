import ast


# TODO
def visit(self, t):
    if isinstance(t.func, ast.Name):
        if t.func.id == 'print':
            visitPrint(self, t)
            return
    self.visit(t.func)
    self.output.write("(")
    comma = False
    for e in t.args:
        if comma: self.output.write(", ")
        else: comma = True
        self.visit(e)
    for e in t.keywords:
        if comma: self.output.write(", ")
        else: comma = True
        self.visit(e)
    if t.starargs:
        if comma: self.output.write(", ")
        else: comma = True
        self.output.write("*")
        self.visit(t.starargs)
    if t.kwargs:
        if comma: self.output.write(", ")
        else: comma = True
        self.output.write("**")
        self.visit(t.kwargs)
    self.output.write(")")


def visitPrint(self, t):
    output = 'std::cout'
    sep = ' '
    end = 'std::endl'
    for e in t.keywords:
        if e.arg == 'sep':
            sep = self.getStr(e.value)
        elif e.arg == 'end':
            end = self.getStr(e.value)
        elif e.arg == 'file':
            pass
    self.write(output)
    for e in t.args:
        self.write("<< %s " % (self.getStr(e)))
        self.write("<< \"%s\" " % sep)
    self.write("<< " + end)
