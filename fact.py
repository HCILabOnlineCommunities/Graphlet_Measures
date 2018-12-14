#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:36:15 2018

@author: miaaltieri
"""

def extraLongFact(n):
    val = n
    n -=1
    while n > 1:
        val*=n
        n-=1
    return val


print (extraLongFact(25))