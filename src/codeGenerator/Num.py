
def visit(self, t):
    repr_n = repr(t.n)
    # Parenthesize negative numbers, to avoid turning (-1)**2 into -1**2.
    if repr_n.startswith("-"):
        self.output.write("(")
    self.output.write(str(t.n))
    # Substitute overflowing decimal literal for AST infinities.
    #self.output.write(repr_n.replace("inf", INFSTR))
    if repr_n.startswith("-"):
        self.output.write(")")
