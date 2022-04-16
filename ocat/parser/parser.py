from ply.yacc import yacc
from .tokenizer import *
from ..ast.nodes import *

# OCat Grammar:
# Program :: statements
# 
# statements :: empty 
#             | statement
#             | statements statement
#
# statement :: declartion
#            | assignment
#            | call
#            | for
#            | if
#
# declaration :: TYPE assignment
#              | MUT TYPE NAME NEWLINE
#              | MUT TYPE assignment
#
# assignment :: NAME ASSIGN expression NEWLINE
#             | NAME ASSIGN call NEWLINE
#
# call :: FUNCNAME LPAREN arguments RPAREN NEWLINE
#
# for :: FOR NAME IN LPAREN arguments RPAREN LOOP statement+ END LOOP NEWLINE 
#
# if :: IF expression THEN statement+ ELSE statement+ END IF NEWLINE
#     | IF expression THEN statement+ END IF NEWLINE
#
# arguments :: empty
#            | expression
#            | arguments COMMA expression
# 
# expression :: expression LSHIFT expression
#             | expression RSHIFT expression
#             | expression BITAND expression
#             | expression BITXOR expression
#             | expression BITOR expression
#             | expression EXP expression
#             | expression MOD expression
#             | expression ADD expression
#             | expression SUB expression
#             | expression MUL expression
#             | expression DIV expression
#             | expression AND expression
#             | expression XOR expression
#             | expression NEQ expression
#             | expression GTE expression
#             | expression LTE expression
#             | expression EQ expression
#             | expression LT expression
#             | expression GT expression
#             | expression OR expression
#             | LPAREN expression RPAREN %prec PAREN
#             | SUB expression
#             | INV expression
#             | NOT expression
#             | NAME DOT NAME
#             | INT
#             | FLOAT
#             | SCI
#             | BOOL
#             | NAME

ocatParser = None

def parse (input):
    global ocatParser
    lexer = lex ()
    lexer.input (input)
    for tok in lexer:
        print (tok)
    lexer = lex ()
    ocatParser = yacc ()
    return ocatParser.parse (input)

# Here lies grammar...
# To abide by code standards, please only use multiline grammars when the logic beneath is very very small

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'NEQ', 'GTE', 'LTE', 'GT', 'LT', 'EQ'),
    ('left', 'BITOR'),
    ('left', 'BITXOR'),
    ('left', 'BITAND'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('right', 'INV'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV', 'MOD'),
    ('right', 'USUB'),
    ('right', 'EXP'),
    ('left', 'PAREN')
)

def p_program (p):
    'program : statements'
    p[0] = Program ('out.bin', p[1])

# Util empty production
def p_empty (p):
    'empty :'
    pass

#################
# Statements
#################

def p_statements (p):
    'statements : statement'
    p[0] = [p[1]]

def p_statements_append (p):
    'statements : statements statement'
    p[1].append (p[2])
    p[0] = p[1]

def p_statements_empty (p):
    'statements : empty'
    p[0] = tuple ()

#################
# Statement
#################

def p_statement (p):
    '''
    statement : declaration
              | assignment
              | call
              | for
              | if
    '''
    p[0] = p[1]

#################
# Declaration
#################

def p_declare (p):
    'declaration : TYPE assignment'
    p[0] = Declare (False, p[1], p[2].target, p[2].expr, p)

def p_declare_mut (p):
    'declaration : MUT TYPE NAME NEWLINE'
    p[0] = Declare (True, p[2], p[3], None, p)

def p_declare_mut_assign (p):
    'declaration : MUT TYPE assignment'
    p[0] = Declare (True, p[2], p[3].target, p[3].expr, p)

#################
# Assignment
#################

def p_assignment (p):
    '''
    assignment : NAME ASSIGN expression NEWLINE
               | NAME ASSIGN call NEWLINE
    '''
    p[0] = Assign (p[1], p[3], p)

#################
# Call
#################

def p_call (p):
    'call : FUNCNAME LPAREN arguments RPAREN NEWLINE'
    p[0] = Function (p[1], p[3], p)

#################
# For
#################

def p_for (p):
    'for : FOR NAME IN LPAREN arguments RPAREN LOOP statements END LOOP NEWLINE'
    p[0] = For (p[2], p[5], p[8], p)

#################
# If
#################

def p_if (p):
    'if : IF expression THEN statements END IF NEWLINE'
    p[0] = If (p[2], p[4], None, p)

def p_if_else (p):
    'if : IF expression THEN statements ELSE statements END IF NEWLINE'
    p[0] = If (p[2], p[4], p[6], p)

#################
# Arguments
#################

def p_arguments (p):
    'arguments : expression'
    p[0] = [p[1]]

def p_arguments_append (p):
    'arguments : arguments COMMA expression'
    p[1].append (p[3])
    p[0] = p[1]

def p_arguments_empty (p):
    'arguments : empty'
    p[0] = tuple ()

#################
# Expression
#################

def p_expr_ternary (p):
    'expression : expression IF expression ELSE expression'
    p[0] = IfExpr (p[3], p[1], p[5], p)

def p_expr_lshift (p):
    'expression : expression LSHIFT expression'
    p[0] = LShift (p[1], p[3], p)

def p_expr_rshift (p):
    'expression : expression RSHIFT expression'
    p[0] = RShift (p[1], p[3], p)

def p_expr_bitand (p):
    'expression : expression BITAND expression'
    p[0] = BitAnd (p[1], p[3], p)

def p_expr_bitxor (p):
    'expression : expression BITXOR expression'
    p[0] = BitXor (p[1], p[3], p)

def p_expr_bitor (p):
    'expression : expression BITOR expression'
    p[0] = BitOr (p[1], p[3], p)

def p_expr_exp (p):
    'expression : expression EXP expression'
    p[0] = Exp (p[1], p[3], p)

def p_expr_mod (p):
    'expression : expression MOD expression'
    p[0] = Mod (p[1], p[3], p)

def p_expr_add (p):
    'expression : expression ADD expression'
    p[0] = Add (p[1], p[3], p)

def p_expr_sub (p):
    'expression : expression SUB expression'
    p[0] = Sub (p[1], p[3], p)

def p_expr_mul (p):
    'expression : expression MUL expression'
    p[0] = Mul (p[1], p[3], p)

def p_expr_div (p):
    'expression : expression DIV expression'
    p[0] = Div (p[1], p[3], p)

def p_expr_and (p):
    'expression : expression AND expression'
    p[0] = And (p[1], p[3], p)

def p_expr_xor (p):
    'expression : expression XOR expression'
    p[0] = Xor (p[1], p[3], p)

def p_expr_neq (p):
    'expression : expression NEQ expression'
    p[0] = Neq (p[1], p[3], p)

def p_expr_gte (p):
    'expression : expression GTE expression'
    p[0] = Gte (p[1], p[3], p)

def p_expr_lte (p):
    'expression : expression LTE expression'
    p[0] = Lte (p[1], p[3], p)

def p_expr_eq (p):
    'expression : expression EQ expression'
    p[0] = Eq (p[1], p[3], p)

def p_expr_lt (p):
    'expression : expression LT expression'
    p[0] = Lt (p[1], p[3], p)

def p_expr_gt (p):
    'expression : expression GT expression'
    p[0] = Gt (p[1], p[3], p)

def p_expr_or (p):
    'expression : expression OR expression'
    p[0] = Or (p[1], p[3], p)

def p_expr_group (p):
    'expression : LPAREN expression RPAREN %prec PAREN'
    p[0] = p[2]

def p_expr_usub (p):
    'expression : SUB expression %prec USUB'
    p[0] = USub (p[2], p)

def p_expr_uinv (p):
    'expression : INV expression'
    p[0] = UInv (p[2], p)

def p_expr_unot (p):
    'expression : NOT expression'
    p[0] = UNot (p[2], p)

def p_expr_dot_name (p):
    'expression : NAME DOT NAME'
    p[0] = Ref (p[1], p, p[3])

def p_expr_name (p):
    'expression : NAME'
    p[0] = Ref (p[1], p)

def p_expr_int (p):
    'expression : INT'
    p[0] = Const (p[1], 'int', p)

def p_expr_float (p):
    'expression : FLOAT'
    p[0] = Const (p[1], 'float', p)

def p_expr_sci (p):
    'expression : SCI'
    p[0] = Const (p[1], 'sci', p)

def p_expr_bool (p):
    'expression : BOOL'
    p[0] = Const (p[1], 'bool', p)


#################
# Error
#################

def p_error (p):
    global ocatParser
    if p:
        if p.type == 'NEWLINE':
        # Ignore any newline characters that are unhandled in our grammar
            ocatParser.errok ()
            return ocatParser.token ()
        print (ocatParser.statestack)
        print (ocatParser.symstack)
        raise SystemExit (f"Syntax error: '{p.value}' on line: {p.lineno}, {p.lexpos}")
    raise SystemExit (f"An unknown error occured while parsing")