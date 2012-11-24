
from ast import NodeVisitor

class NodeFinder(NodeVisitor):

    def __init__(self):
        self.nodes = []
        self.res = []
        self.stopFirst = False
        self.stop = False

    def visit(self, tree):
        if self.stop:
            return
        if isinstance(tree, list):
            for node in tree:
                self.visit(node)
        else:
            name = tree.__class__.__name__
            if name in self.nodes:
                self.res.append(tree)
                if self.stopFirst:
                    self.stop = True
                    return

            self.generic_visit(tree)


    def findFirst(self, tree, nodeNames):
        self.nodes = nodeNames
        self.res = []
        self.stopFirst = True
        self.stop = False
        self.visit(tree)
        if self.res:
            return self.res[0]
        else:
            return None

    def findAll(self, tree, nodeNames):
        self.nodes = nodeNames
        self.res = []
        self.stopFirst = True
        self.stop = False
        self.visit(tree)
        return self.res
