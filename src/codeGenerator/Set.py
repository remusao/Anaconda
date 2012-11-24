
def visit(self, t):
    self.includes.add("set")
    assert(t.elts) # should be at least one element

    # Find type of the keys
    self.output.stackBuffer()
    self.visit(t.elts[0])
    type = self.output.topPop().getvalue()

    self.output.write("std::set<decltype (%s)>" % (type))
    self.enterScope()
    self.output.fill()
    self.interLeave(lambda: self.output.write(", "), self.visit, t.elts)
    self.leaveScope(None, "")
