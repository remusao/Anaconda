#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DefaultVisitor:
    """General visitor"""
    
    def visit(self, node):
        """Visit a node"""
        # Find a specific visit method, default to "default"
        methname = "visit_%s" % node.__class__.__name__
        method = getattr(self, methname, self.default)

        # Call visit method on node
        method(node)

    def default(self, node):
        """Visit node children"""
        for child in node.children:
            self.visit(child)