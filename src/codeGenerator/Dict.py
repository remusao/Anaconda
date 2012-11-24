
# TODO : Handle empty dic
def visit(self, t):
    self.includes.add("unordered_map")

    # Find type of the keys
    self.output.stackBuffer()
    self.visit(t.values[0])
    type1 = self.output.topPop().getvalue()

    # Find type of the values
    self.output.stackBuffer()
    self.visit(t.keys[0])
    type2 = self.output.topPop().getvalue()

    # declare the type
    self.output.write("std::unordered_map<decltype (%s), decltype (%s)>"
                         % (type1, type2))
    self.enterScope()
    def write_pair(pair):
        (k, v) = pair
        self.output.fill()
        self.output.write("{")
        self.visit(k)
        self.output.write(", ")
        self.visit(v)
        self.output.write("}")
    self.interLeave(lambda: self.output.write(", "), write_pair,
                        list(zip(t.keys, t.values)))
    self.leaveScope(None, "")
