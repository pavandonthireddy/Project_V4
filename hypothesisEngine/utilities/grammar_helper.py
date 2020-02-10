# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 00:19:45 2020

@author: Pavan
"""


import os



def grammar_helper(string):
    file1= open('.\\hypothesisEngine\\grammar\\current_grammar.bnf','w')
    file1.write(string)
    file1.close()