#!/usr/bin/env python
# -*- coding: utf-8 -*-

def myrange():
    for i in range(1, 10, 2):
        yield i

def main():
    for x in myrange():
        print(x)

main()
