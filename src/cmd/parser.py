from ply.yacc import yacc
from .tokenizer import *
from .ast.nodes import *

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

# --- Parser
def p_progam (p):
    '''
    seq : statement
        | seq statement
        
    '''
    if len (p) == 2:
        p[0] = Seq ("out.seq", [p[1]])
    elif len (p) == 3:
        p[1].statements.append (p[2])
        p[0] = p[1]

def p_statement (p):
    '''
    statement : declare
              | assign
              | procedure
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
    p[0] = Assign (p[1], p[3])

def p_expression (p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | group
               | unary
               | function
               | NAME
               | NUMBER
    '''
    if len (p) == 4:
        p[0] = p[2] (p[1], p[3])
    elif len (p) == 2:
        p[0] = p[1]

def p_group (p):
    '''
    group : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_function (p):
    '''
    function : FUNCNAME LPAREN arguments RPAREN
    '''
    p[0] = Function (p[1], p[3])

def p_procedure (p):
    '''
    procedure : PROCNAME LPAREN arguments RPAREN
    '''
    p[0] = Procedure (p[1], p[3])

def p_arguments (p):
    '''
    arguments : expression
              | arguments SEPERATOR expression
    '''
    if len (p) == 2:
        p[0] = [p[1]]
    elif len (p) == 4:
        p[1].append (p[3])
        p[0] = p[1]

def p_unary_sub (p):
    '''
    unary : MINUS expression
    '''
    p[0] = UnarySub (p[2])

def p_error(p):
    raise Exception (f"Syntax error: '{p.value}' at line: {p.lineno}, pos: {p.lexpos}")

def parse (input):
    return yacc ().parse (input)