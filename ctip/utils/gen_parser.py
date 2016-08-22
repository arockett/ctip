# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 11:27:43 2016

@author: Aaron Beckett
"""

data = """
# comment
bows # comment
type = long, recurve
type = long
    length = 65, 68
# comment
wood = osage orange, "#, not", comment
# comment
"""

import pyparsing as p
import pprint

def GenParser():
    """
    Create parser for genfile using pyparsing library.
    
    Returns:
        Parser capable of turning a genfile into a consumable ParseResults object.
    """
    
    def strip_quotes(s):
        """Strip quotation marks from the end of a string if present."""
        if isinstance(s, str) and len(s) > 1:
            if (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"):
                s = s[1:-1]
        return s
        
    def clean_csv(s, loc, toks):
        """Parse action that strips quotation marks from any string tokens."""
        return [strip_quotes(tok) for tok in toks]
        
    # Indent stack needed for the pyparsing indentBlock function
    indent_stack = [1]
    # Statement used for recursive definition of genfile grammar
    stmt = p.Forward()

    # Define comment structure    
    comment = "#" + p.restOfLine

    # Variable names must start with a letter and can include
    # numbers, dashes, underscores, and periods.
    variable = p.Word(p.alphas, p.alphanums + "-_.")
    
    # Comma separated list of values
    values = p.commaSeparatedList.addParseAction(clean_csv)

    # Variable domain/scope:
    #       variable = val1, val2, val3 ...
    scope = variable("var") + p.Suppress("=") + p.Group(values)("values")
    
    # Dependencies are variable domains nested beneath another scope
    deps = p.indentedBlock(stmt, indent_stack)
    
    # A suite is a variable scope along with all of its dependencies
    suite = scope + p.Optional(deps)("deps")
    stmt << suite
    
    # A gen schema is one or more suites of variables
    genschema = p.OneOrMore(p.Group(suite))
    
    # A genfile starts with an optional schema name then defines a gen schema
    genfile = p.Optional(variable) + genschema
    # Ignore comments in genfile
    genfile.ignore(comment)
    
    return genfile
    
GenParser = GenParser()

r = None
try:
    r = GenParser.parseString(data)
    pprint.pprint(r.asList())
except p.ParseException as err:
    print(err.line)
    print(" "*(err.column-1) + "^")
    print(err)