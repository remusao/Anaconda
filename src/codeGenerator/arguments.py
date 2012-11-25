
# TODO
def visit(self, t):
    first = True
    count = 0
    # normal arguments
    defaults = [None] * (len(t.args) - len(t.defaults)) + t.defaults
    for a, d in zip(t.args, defaults):
        if first:
            first = False
        else:
            self.output.write(", ")
        self.output.write("T%i " % (count))
        self.variablesInScope[-1].add(a.arg)
        self.visit(a)
        count += 1
        if d:
            self.output.write("=")
            self.visit(d)

    # TODO
    # varargs
    if t.vararg:
        if first:first = False
        else: self.output.write(", ")
        self.output.write("*")
        self.output.write(t.vararg)

    # TODO
    # kwargs
    if t.kwarg:
        if first:first = False
        else: self.output.write(", ")
        self.output.write("**"+t.kwarg)
