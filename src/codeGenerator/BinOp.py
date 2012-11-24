
binop = {
    "Add" : "+",
    "Sub" : "-",
    "Mult" : "*",
    "Div" : "/",
    "Mod" : "%",
    "LShift" : "<<",
    "RShift" : ">>",
    "BitOr" : "|",
    "BitXor" : "^",
    "BitAnd" : "&",
    "FloorDiv" : "//",
    "Pow" : "**"
}



def visit(self, t):
    self.visit(t.left)
    self.output.write(" %s " % (binop[t.op.__class__.__name__]))
    self.visit(t.right)
