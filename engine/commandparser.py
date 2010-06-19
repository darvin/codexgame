# -*- coding:utf-8 -*-

from pyparsing import *

# =======================================================

pIdent = Group(Word(alphas, alphanums+'_')).setResultsName('ident')
pInt = Combine( Optional( Word('+-', exact=1) ) + Word(nums) ).setResultsName('int')
pStr = quotedString.setResultsName('str')

pObject = Group(Literal('<').suppress() + Word(alphas, alphanums+'_') + Word(nums) + Literal('>').suppress())
pList = Forward()

pVars = pObject | pList | pInt | pStr
pList << Group(Literal('[').suppress() + delimitedList(pVars) + Literal(']').suppress()).setResultsName('list')

pExec = Group(Suppress('(') + Optional(delimitedList(pVars)) + Suppress(')')).setResultsName('exec')
pGetItem = Group(Suppress('[') + delimitedList(pVars) + Suppress(']')).setResultsName('get')
pGetAttr = Literal('.').suppress() + pIdent

pExpression = (pIdent + ZeroOrMore(pExec | pGetItem | pGetAttr)).setResultsName('object')

# =======================================================

def parse(s):
	return pExpression.parseString(s)

