# indentedGrammarExample.py
#
# Copyright (c) 2006, Paul McGuire
#
# A sample of a pyparsing grammar using indentation for 
# grouping (like Python does).
#

import pyparsing as p

data = """\
def A(z):
  A1
  B = 100
  G = A2
  A2
  A3
B
def BB(a,b,c):
  BB1
  def BBA():
    bba1
    bba2
    bba3
C
D
def spam(x,y):
     def eggs(z):
         pass
"""

indentStack = [1]

def checkPeerIndent(s,loc,toks):
    curCol = p.col(loc,s)
    if curCol != indentStack[-1]:
        if (not indentStack) or curCol > indentStack[-1]:
            raise p.ParseFatalException(s,loc,"illegal nesting")
        raise p.ParseException(s,loc,"not a peer entry")

def checkSubIndent(s,loc,toks):
    curCol = p.col(loc,s)
    if curCol > indentStack[-1]:
        indentStack.append( curCol )
    else:
        raise p.ParseException(s,loc,"not a subentry")

def checkUnindent(s,loc,toks):
    if loc >= len(s): return
    curCol = p.col(loc,s)
    if not(curCol < indentStack[-1] and curCol <= indentStack[-2]):
        raise p.ParseException(s,loc,"not an unindent")

def doUnindent():
    indentStack.pop()
    
INDENT = p.lineEnd.suppress() + p.empty + p.empty.copy().setParseAction(checkSubIndent)
UNDENT = p.FollowedBy(p.empty).setParseAction(checkUnindent)
UNDENT.setParseAction(doUnindent)

stmt = p.Forward()
suite = p.Group( p.OneOrMore( p.empty + stmt.setParseAction( checkPeerIndent ) )  )

identifier = p.Word(p.alphas, p.alphanums)
funcDecl = ("def" + identifier + p.Group( "(" + p.Optional( p.delimitedList(identifier) ) + ")" ) + ":")
funcDef = p.Group( funcDecl + INDENT + suite + UNDENT )

rvalue = p.Forward()
funcCall = p.Group(identifier + "(" + p.Optional(p.delimitedList(rvalue)) + ")")
rvalue << (funcCall | identifier | p.Word(p.nums))
assignment = p.Group(identifier + "=" + rvalue)
stmt << ( funcDef | assignment | identifier )

print(data)
parseTree = suite.parseString(data)

import pprint
pprint.pprint( parseTree.asList() )
