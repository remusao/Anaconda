
def visit(self, t):
    self.includes.add("cassert")
    self.output.fill("assert(")
    self.visit(t.test)
    #if t.msg:
    #    self.output.write(", ")
    #    self.visit(t.msg)
    self.output.write(");")
