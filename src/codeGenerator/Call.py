
# TODO
def visit(self, t):
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
