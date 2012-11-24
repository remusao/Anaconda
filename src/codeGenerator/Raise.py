
def visit(self, t):
    if t.exc:
        self.output.fill('throw ' + t.exc)
