from mimetypes import types_map
from ply.lex import lex
from .ast.nodes import *

# --- Tokenizer

# All tokens must be named in advance.
tokens = ( 'TYPE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
           'NAME', 'NUMBER', 'ASSIGN', 'PROCNAME', 'FUNCNAME', 'SEPERATOR' )

# Plain tokens
t_ignore = ' \t'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_SEPERATOR = r','

# Type tokens
reserved_words = {
    'int' : 'TYPE',
    'uint' : 'TYPE',
    'float' : 'TYPE',
    'command' : 'PROCNAME',
    'print' : 'PROCNAME',
    'fetch' : 'FUNCNAME'
}

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMBER(t):
    r'\d+'
    t.value = Number (t.value)
    return t

def t_NAME (t):
    r'[a-zA-Z]+[a-zA-Z0-9_]*'
    if t.value in reserved_words:
        t.type = reserved_words[t.value]
    else:
        t.value = Name (t.value)
    return t

def t_PLUS (t):
    r'\+'
    t.value = Add
    return t

def t_MINUS (t):
    r'-'
    t.value = Sub
    return t

def t_TIMES (t):
    r'\*'
    t.value = Mult
    return t

def t_DIVIDE (t):
    r'/'
    t.value = Div
    return t

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    raise Exception (f"Illegal Character: '{t.value[0]}' at line: {t.lineno}, pos: {t.lexpos}")

lexer = lex ()