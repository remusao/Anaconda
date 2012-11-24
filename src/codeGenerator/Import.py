
# TODO : check if it's standard lib or a file in the project
def visit(self, t):
    for name in t.names:
        self.includes.add(name.name)
