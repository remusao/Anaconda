
def visit(self, t):
    self.includes.add("vector")

    # Find type of the elements
    self.output.stackBuffer()
    self.visit(t.elts[0])
    type = self.output.topPop().getvalue()

    self.output.write("std::vector<decltype (%s)>" % (type))
    self.enterScope()
    self.output.fill()
    self.interLeave(lambda: self.output.write(", "), self.visit, t.elts)
    self.leaveScope(None, "")
