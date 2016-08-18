# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 11:27:43 2016

@author: Aaron Beckett
"""

data = """
# comment
bows # comment
# type = long, recurve
# comment
wood = osage orange, yew, oak, hickory, '#', not comment
# comment
"""

import pyparsing as p

def join_tokens(s, loc, toks):
    return ''.join(toks)

variable = p.Word(p.alphas, p.alphanums + "-_.")

var_def = p.Dict(p.Group(variable + p.Suppress("=") + p.commaSeparatedList))

genschema = p.OneOrMore(var_def)
genfile = variable + genschema

# Remove comments
cleaned = p.pythonStyleComment.suppress().transformString(data)

# Parse cleaned string
r = genfile.parseString(cleaned)
