from BinOp import binop

def visit(self, t):
    self.output.fill()
    self.visit(t.target)
    self.output.write(" %s= " % (self.binop[t.op.__class__.__name__]))
    self.visit(t.value)
    self.output.write(";")
