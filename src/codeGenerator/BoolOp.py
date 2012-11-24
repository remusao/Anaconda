
    boolop = {
        ast.And : '&&',
        ast.Or : '||'
    }


def visit(self, t):
    s = " %s " % self.boolop[t.op.__class__]
    self.interLeave(lambda: self.output.write(s), self.visit, t.values)
