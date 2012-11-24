

def visit(self, tree):
    if isinstance(tree.s, str):
        self.output.write('"%s"' % (tree.s))
    elif isinstance(tree.s, unicode):
        self.output.write(repr(tree.s).lstrip("u"))
    else:
        assert False, "shouldn't get here"

