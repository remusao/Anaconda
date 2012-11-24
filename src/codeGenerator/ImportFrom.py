
# TODO : check if it's standard lib or a file in the project
def visit(self, t):
    module = '/'
    if t.module:
        module += t.module
    self.includes.add("%s%s" % ('.' * t.level, t.module))
    #for name in t.names:
    #    self.includes.add("%s%s/%s" % ('.' * t.level, t.module, name.name))
