
import ast

def visit(self, t):
    self.visit(t.value)
    # Special case: 3.__abs__() is a syntax error, so if t.value
    # is an integer literal then we need to either parenthesize
    # it or add an extra space to get 3 .__abs__().
    if isinstance(t.value, ast.Num) and isinstance(t.value.n, int):
        self.output.write(" ")
    self.output.write(".")
    self.output.write(t.attr)
