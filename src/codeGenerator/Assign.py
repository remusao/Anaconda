import ast

def visit(self, t):
    for target in t.targets:
        self.output.fill()
        if isinstance(target, ast.Name):
            if target.id not in self.variablesInScope[-1]:
                self.variablesInScope[-1].add(target.id)
                self.output.write("auto ")
        self.visit(target)
        self.output.write(" = ")
        self.visit(t.value)
        self.output.write(";")
