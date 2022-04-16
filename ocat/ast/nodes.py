from enum import Enum

class Program:
    def __init__ (self, id, statements):
        self.id = id
        self.statements = statements

    def __repr__ (self):
        return  f"{type(self).__name__}({self.id}, {self.statements})"
       
class Declare:
    def __init__ (self, mutable, type, name, expr, token):
        self.mutable = mutable
        self.type = type
        self.name = name
        self.expr = expr
        self.token = token
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.mutable}, {self.type}, {self.name}, {self.expr})"

class Assign:
    def __init__ (self, target, expr, token):
        self.target = target
        self.expr = expr
        self.token = token

    def __repr__ (self):
        return f"{type(self).__name__}({self.target}, {self.expr})"

class Function:
    def __init__ (self, name, args, token):
        self.name = name
        self.args = args
        self.token = token

    def __repr__ (self):
        return f"{type(self).__name__}({self.name}, {self.args})"

class If:
    def __init__ (self, condition, then, else_, token):
        self.condition = condition
        self.then = then
        self.else_ = else_
        self.token = token

    def __repr__ (self):
        return f"{type(self).__name__}({self.condition}, {self.then}, {self.else_})"

class IfExpr:
    def __init__ (self, condition, then, else_, token):
        self.condition = condition
        self.then = then
        self.else_ = else_
        self.token = token
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.condition}, {self.then}, {self.else_})"

class For:
    def __init__ (self, iterator, args, statements, token):
        self.iterator = iterator
        self.args = args
        self.statements = statements
        self.token = token

    def __repr__ (self):
        return f"{type(self).__name__}({self.iterator}, {self.args}, {self.statements})"

class Const:
    def __init__ (self, value, type, token):
        self.value = value
        self.type = type
        self.toke = token
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.type}, {self.value})"

class Ref:
    def __init__ (self, name, token, dot = None):
        self.name = name
        self.token = token
        self.dot = dot
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.name}, {self.dot})"

class BinOp:
    def __init__ (self, left, right, token):
        self.left = left
        self.right = right
        self.token = token
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.left}, {self.right})"

class LShift (BinOp):
    pass

class RShift (BinOp):
    pass

class BitAnd (BinOp):
    pass

class BitXor (BinOp):
    pass

class BitOr (BinOp):
    pass

class Exp (BinOp):
    pass

class Mod (BinOp):
    pass

class Add (BinOp):
    pass

class Sub (BinOp):
    pass

class Mul (BinOp):
    pass

class Div (BinOp):
    pass

class Eq (BinOp):
    pass

class Neq (BinOp):
    pass

class And (BinOp):
    pass

class Or (BinOp):
    pass

class Xor (BinOp):
    pass

class Gte (BinOp):
    pass

class Lte (BinOp):
    pass

class Lt (BinOp):
    pass

class Gt (BinOp):
    pass

class UnaryOp:
    def __init__ (self, expr, token):
        self.expr = expr
        self.token = token
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.expr})"

class USub (UnaryOp):
    pass

class UInv (UnaryOp):
    pass

class UNot (UnaryOp):
    pass
