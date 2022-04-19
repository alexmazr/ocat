from ply.lex import lex
from ctypes import *
from ..settings import Settings

# --- Tokenizer
# The rules for each token are evaluated top to bottom in this file (ply evaluates functions first, in order, than the single line plain tokens)
tokens = ( 'TYPE', 'INT', 'UINT', 'FLOAT', 'FUNCNAME', 'LOOP', 'END', 'FOR', 'IF', 'ELSE', 
            'THEN', 'MUT', 'LPAREN', 'RPAREN', 'COMMA', 'NEWLINE', 'IN', 'WAIT', 'TIMEOUT',
            'ASSIGN', 'DOT', 'NAME', 'NOT', 'AND', 'XOR', 'OR', 'LSHIFT', 'RETURN', 'WITH',
            'RSHIFT', 'BITAND', 'BITXOR', 'BITOR', 'EXP', 'MOD', 'ADD', 'WAITTYPE',
            'SUB', 'MUL', 'DIV', 'NEQ', 'GTE', 'LTE', 'EQ', 'LT', 'GT', 'INV', 'TRUE', 'FALSE' )

settings = Settings ()

# Special Reserved words
reserved_words = {
    'int' : 'TYPE',
    'uint' : 'TYPE',
    'float' : 'TYPE',
    'bool' : 'TYPE',
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
    'true' : 'TRUE',
    'false' : 'FALSE',
    'in' : 'IN',
    'wait' : 'WAIT',
    'rel' : 'WAITTYPE',
    'abs' : 'WAITTYPE',
    'with' : 'WITH',
    'timeout' : 'TIMEOUT',
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

def t_FLOAT (t):
    r'(-{0,1}\d+(\.\d+|\d*)e(\+|-)\d+|-{0,1}\d+\.\d+)'
    global settings
    try:
        t.value = settings.ocat_float (float (t.value))
        return t
    except:
        raise SystemExit (f"Constant float '{t.value}' out of range: {t.lineno}, {t.lexpos}")

def t_INT (t):
    r'-\d+'
    global settings
    try:
        t.value = settings.ocat_int (int (t.value))
        return t
    except:
        raise SystemExit (f"Constant int '{t.value}' out of range: {t.lineno}, {t.lexpos}")

def t_UINT (t):
    r'\d+'
    global settings
    try:
        t.value = settings.ocat_uint (int (t.value))
        return t
    except:
        raise SystemExit (f"Constant uint '{t.value}' out of range: {t.lineno}, {t.lexpos}")

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