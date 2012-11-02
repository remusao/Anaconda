#!/usr/bin/env python
# -*- coding: utf-8 -*-

def myrange():
    yield 42
    yield 1138
    for i in [1, 2, 3, 4]:
        yield i

def main():
    for x in myrange():
        print(x)

main()
