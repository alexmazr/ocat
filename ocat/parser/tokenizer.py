from ply.lex import lex
from ..ast.nodes import *

# --- Tokenizer
# The rules for each token are evaluated top to bottom in this file (ply evaluates functions first, in order, than the single line plain tokens)
tokens = ( 'TYPE', 'BOOL', 'INT', 'UINT', 'FLOAT', 'SCI', 'FUNCNAME', 'LOOP', 'END', 'FOR', 'IF', 'ELSE', 
            'THEN', 'MUT', 'LPAREN', 'RPAREN', 'COMMA', 'NEWLINE', 'IN', 'WAIT', 'UNTIL',
            'ASSIGN', 'DOT', 'NAME', 'NOT', 'AND', 'XOR', 'OR', 'LSHIFT', 'RETURN',
            'RSHIFT', 'BITAND', 'BITXOR', 'BITOR', 'EXP', 'MOD', 'ADD', 
            'SUB', 'MUL', 'DIV', 'NEQ', 'GTE', 'LTE', 'EQ', 'LT', 'GT', 'INV' )

# Special Reserved words
reserved_words = {
    'int' : 'TYPE',
    'uint' : 'TYPE',
    'float' : 'TYPE',
    'sci' : 'TYPE',
    'bool' : 'TYPE',
    'tlm' : 'TYPE',
    'send' : 'FUNCNAME',
    'fetch_new' : 'FUNCNAME',
    'fetch' : 'FUNCNAME',
    'loop' : 'LOOP',
    'end' : 'END',
    'for' : 'FOR',
    'if' : 'IF',
    'else' : 'ELSE',
    'then' : 'THEN',
    'mut' : 'MUT',
    'not' : 'NOT',
    'and' : 'AND',
    'xor' : 'XOR',
    'or' : 'OR',
    'true' : 'BOOL',
    'false' : 'BOOL',
    'in' : 'IN',
    'wait' : 'WAIT',
    'until' : 'UNTIL',
    'return' : 'RETURN'
}

# Match and ignore a comment before any other rule
def t_COMMENT (t):
     r'\#.*'
     pass

def t_NAME (t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved_words.get (t.value, 'NAME')
    return t

def t_SCI (t):
    r'\d+e-{0,1}\d+'
    return t

def t_FLOAT (t):
    r'\d+\.\d+'
    try:
        t.value = float (t.value)
        return t
    except:
        raise SystemExit (f"FLOAT constant too large at: {t.lineno}, {t.lexpos}")

def t_UINT (t):
    r'-\d+'
    try:
        t.value = int (t.value)
        return t
    except:
        raise SystemExit (f"UINT constant too large at: {t.lineno}, {t.lexpos}")

def t_INT (t):
    r'\d+'
    try:
        t.value = int (t.value)
        return t
    except:
        raise SystemExit (f"INT constant too large at: {t.lineno}, {t.lexpos}")

def t_NEWLINE (t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t
    
# Double length tokens, matched before single length
t_RSHIFT = r'>>'
t_LSHIFT = r'<<'
t_GTE = r'>='
t_LTE = r'<='
t_EQ = r'=='
t_EXP = r'\*\*'

# Single length tokens, matched last
t_ignore = ' \t'
t_BITXOR = r'\^'
t_BITAND = r'&'
t_BITOR = r'\|'
t_MOD = r'%'
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_DOT = r'\.'
t_COMMA = r','
t_LT = r'<'
t_GT = r'>'
t_INV = r'~'

def t_error (t):
     raise SystemExit (f"Illegal character: {t.value[0]} at: {t.lineno}, {t.lexpos}")