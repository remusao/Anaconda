
def visit(self, t):
    self.includes.add("vector")

    if len(t.elts) != 0:
        # Find type of the elements
        self.output.stackBuffer()
        self.visit(t.elts[0])
        type = self.output.topPop().getvalue()
    else:
        type = 'double'

    self.output.write("std::vector<decltype (%s)>" % (type))
    self.enterScope()
    self.output.fill()
    self.interLeave(lambda: self.output.write(", "), self.visit, t.elts)
    self.leaveScope(None, "")
