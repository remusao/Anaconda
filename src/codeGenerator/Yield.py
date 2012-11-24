
# TODO : use coroutine
def visit(self, t):
    self.output.write("yield")
    if t.value:
        self.output.write(" return ")
        self.visit(t.value)
    #self.output.write("(")
    #self.output.write("yield")
    #if t.value:
    #    self.output.write(" ")
    #    self.visit(t.value)
    #self.output.write(")")
