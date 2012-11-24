
# TODO
def visit(self, t):
    if t.lower:
        self.visit(t.lower)
        self.output.write(":")
    if t.upper:
        self.visit(t.upper)
    if t.step:
        self.output.write(":")
        self.visit(t.step)
