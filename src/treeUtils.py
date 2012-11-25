
from ast import NodeVisitor, NodeTransformer
import ast


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

            getattr(self, "visit_%s" % (tree.__class__.__name__),
                    self.generic_visit)(tree)


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




class TreeSize(NodeVisitor):
    """
        Count the number of nodes in the tree
    """

    def __init__(self):
        self.size = 0

    def visit(self, tree):
        if isinstance(tree, list):
            for node in tree:
                self.visit(node)
        else:
            getattr(self, "visit_%s" % (tree.__class__.__name__),
                    self.generic_visit)(tree)


    def __call__(self, tree):
        self.size = 0
        self.visit(tree)
        return self.size



class AllInScope(NodeVisitor):
    """
        Check if all the identifiers in the tree
        are known in the current scope
    """

    def __init__(self):
        self.scope = set([])
        self.notInScope = []


    def visit(self, tree):
        if isinstance(tree, list):
            for node in tree:
                self.visit(node)
        else:
            getattr(self, "visit_%s" % (tree.__class__.__name__),
                    self.generic_visit)(tree)


    def visit_Name(self, tree):
        if isinstance(tree.ctx, ast.Load) and (tree.id not in self.scope):
            self.notInScope.append(tree)


    def __call__(self, tree, scope):
        self.scope = scope
        self.notInScope = []
        self.visit(tree)
        return self.notInScope



class GetDefinition(NodeVisitor):
    """
        Find the definition of the variable
        name into the given tree
    """

    def __init__(self):
        self.found = False
        self.quit = False
        self.res = None
        self.name = None

    def visit(self, tree):
        if self.quit:
            return
        if isinstance(tree, list):
            for node in tree:
                if not self.quit:
                    self.visit(node)
        else:
            getattr(self, "visit_%s" % (tree.__class__.__name__),
                    self.generic_visit)(tree)


    def visit_Name(self, tree):
        if tree.id == self.name:
            self.found = True
            self.quit = True


    def visit_Assign(self, tree):
        for target in tree.targets:
            self.visit(target)
            if self.found:
                self.res = tree.value
                break


    def __call__(self, tree, name):
        self.found = False
        self.quit = False
        self.res = None
        self.name = name
        self.visit(tree)
        return self.res



class ReplaceNode(NodeTransformer):
    """
        Replace all the occurences of ast.Name with
        the given name by the given Node (insteadOfName)
    """

    def __init__(self):
        self.name = None
        self.insteadOfName = None
        self.quit = False


    def visit_Name(self, tree):
        if tree.id == self.name:
            return ast.copy_location(self.insteadOfName, tree)
        else:
            return tree


    def __call__(self, name, insteadOfName, tree):
        self.name = name
        self.insteadOfName = insteadOfName
        self.quit = False
        return self.visit(tree)
