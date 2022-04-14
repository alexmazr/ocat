from ply.lex import lex
from ply.yacc import yacc
from nodes import *

# --- Tokenizer

# All tokens must be named in advance.
tokens = ( 'TYPE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
           'NAME', 'NUMBER', 'ASSIGN',  )

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME (t):
    r'[a-zA-Z]+[a-zA-Z0-9_]*'
    if t.value == 'int' or t.value == 'uint' or t.value == 'float':
        t.type = 'TYPE'
    
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    raise Exception (f"Illegal Character: '{t.value[0]}' at line: {t.lineno}, pos: {t.lexpos}")

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

# --- Parser
def p_progam (p):
    '''
    seq : statement
        
    '''
    p[0] = Seq ("out.seq", [p[1]])

def p_program_append (p):
    '''
    seq : seq statement
    '''
    p[1].statements.append (p[2])
    p[0] = p[1]

def p_statement (p):
    '''
    statement : declare
              | assign
    '''
    p[0] = p[1]

def p_declare (p):
    '''
    declare : TYPE NAME
            | TYPE assign
    '''
    p[0] = Declare (p[1], p[2])

def p_assign (p):
    '''
    assign : NAME ASSIGN expression
    '''
    p[0] = Assign (Name (p[1]), p[3])

def p_expr_plus (p):
    '''
    expression : expression PLUS expression
    '''
    p[0] = Add (p[1], p[3])

def p_expr_minus (p):
    '''
    expression : expression MINUS expression
    '''
    p[0] = Sub (p[1], p[3])

def p_expr_times (p):
    '''
    expression : expression TIMES expression
    '''
    p[0] = Mult (p[1], p[3])

def p_expr_divide (p):
    '''
    expression : expression DIVIDE expression
    '''
    p[0] = Div (p[1], p[3])

def p_expr_paren (p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_expr_name (p):
    '''
    expression : NAME
    '''
    p[0] = Name (p[1])

def p_expr_number (p):
    '''
    expression : NUMBER
    '''
    p[0] = Number (p[1])

def p_expr_unary (p):
    '''
    expression : unary
    '''
    p[0] = p[1]

def p_unary(p):
    '''
    unary : MINUS NAME
           | MINUS NUMBER
    '''
    p[0] = -p[2]

def p_error(p):
    raise Exception (f"Syntax error: '{p.value}' at line: {p.lineno}, pos: {p.lexpos}")

def parse (input, debug = False):
    lexer = lex ()
    parser = yacc ()

    if debug:
        lexer.input (input)
        for tok in lexer:
            print (tok)

    return parser.parse (input)