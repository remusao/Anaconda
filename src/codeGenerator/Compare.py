
cmpops = {
    "Eq" : "==",
    "NotEq" : "!=",
    "Lt" : "<",
    "LtE" : "<=",
    "Gt" : ">",
    "GtE" : ">=",
    "Is" : "==",
    "IsNot" : "!=",
    "In" : "in",
    "NotIn" : "not in"
}


def visit(self, t):
    self.visit(t.left)
    for o, e in zip(t.ops, t.comparators):
        self.output.write(" %s " % (cmpops[o.__class__.__name__]))
        self.visit(e)
