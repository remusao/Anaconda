#!/usr/bin/env python
# -*- coding: utf-8 -*-

def myrange():
    for i in [1, 2, 3, 4]:
        yield i

def main():
    for x in myrange():
        print(x)

main()
