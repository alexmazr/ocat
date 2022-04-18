from enum import Enum

class Program:
    def __init__ (self, id, statements):
        self.id = id
        self.statements = statements

    def __repr__ (self):
        return  f"{type(self).__name__}({self.id}, {self.statements})"

class EndProgram:
    isFlat = False

    def __init__ (self, args, linedata):
        self.args = args
        self.linedata = linedata

    def __repr__ (self):
        return  f"{type(self).__name__}({self.args})"

class LineData:
    def __init__ (self, lineno, linepos):
        self.lineno = lineno
        self.linepos = linepos

class Declare:
    isFlat = False

    def __init__ (self, mutable, type, name, expr, linedata):
        self.mutable = mutable
        self.type = type
        self.name = name
        self.expr = expr
        self.linedata = linedata
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.mutable}, {self.type}, {self.name}, {self.expr})"

class Assign:
    isFlat = False

    def __init__ (self, name, expr, linedata):
        self.name = name
        self.expr = expr
        self.linedata = linedata

    def __repr__ (self):
        return f"{type(self).__name__}({self.name}, {self.expr})"

class Call:
    isFlat = False

    def __init__ (self, name, args, linedata):
        self.name = name
        self.args = args
        self.linedata = linedata

    def __repr__ (self):
        return f"{type(self).__name__}({self.name}, {self.args})"

class Wait:
    isFlat = True

    def __init__ (self, type, time, linedata):
        self.type = type
        self.time = time
        self.linedata = linedata

    def __repr__ (self):
        return f"{type(self).__name__}({self.type}, {self.time})"

class If:
    isFlat = False

    def __init__ (self, condition, then, else_, linedata):
        self.condition = condition
        self.then = then
        self.else_ = else_
        self.linedata = linedata

    def __repr__ (self):
        return f"{type(self).__name__}({self.condition}, {self.then}, {self.else_})"

class IfExpr:
    isFlat = False

    def __init__ (self, condition, then, else_, linedata):
        self.condition = condition
        self.then = then
        self.else_ = else_
        self.linedata = linedata
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.condition}, {self.then}, {self.else_})"

class Jump:
    def __init__ (self, pc):
        self.pc = pc
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.pc})"

class Exec (Jump):
    pass

class Ret (Jump):
    pass

class For:
    isFlat = False

    def __init__ (self, iterator, args, statements, linedata):
        self.iterator = iterator
        self.args = args
        self.statements = statements
        self.linedata = linedata

    def __repr__ (self):
        return f"{type(self).__name__}({self.iterator}, {self.args}, {self.statements})"

class Const:
    isFlat = True

    def __init__ (self, value, type, linedata):
        self.value = value
        self.type = type
        self.toke = linedata
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.type}, {self.value})"

class Ref:
    isFlat = True

    def __init__ (self, name, linedata, dot = None):
        self.name = name
        self.linedata = linedata
        self.dot = dot
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.name}, {self.dot})"

class BinOp:
    isFlat = False

    def __init__ (self, left, right, linedata):
        self.left = left
        self.right = right
        self.linedata = linedata

    def reduce (self):
        print (f"Optimization for {type(self).__name__} not available.")
        return self

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
    def reduce (self):
        if isinstance (self.left, Const) and isinstance (self.right, Const):
            result = self.left.value + self.right.value
            if isinstance (result, float):
                return Const (result, 'float', None)
            if result >= 0:
                return Const (result, 'int', None)
            else:
                return Const (result, 'uint', None)
        return self

class Sub (BinOp):
    pass

class Mul (BinOp):
    def reduce (self):
        if isinstance (self.left, Const) and isinstance (self.right, Const):
            result = self.left.value * self.right.value
            if isinstance (result, float):
                return Const (result, 'float', None)
            if result >= 0:
                return Const (result, 'int', None)
            else:
                return Const (result, 'uint', None)
        return self

class Div (BinOp):
    pass

class Eq (BinOp):
    def reduce (self):
        if isinstance (self.left, Const) and isinstance (self.right, Const):
            return Const (self.left.value == self.right.value, 'bool', None)
        return self

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
    def reduce (self):
        if isinstance (self.left, Const) and isinstance (self.right, Const):
            return Const (self.left.value < self.right.value, 'bool', None)
        return self

class Gt (BinOp):
    pass

class UnaryOp:
    isFlat = False

    def __init__ (self, expr, linedata):
        self.expr = expr
        self.linedata = linedata
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.expr})"

class USub (UnaryOp):
    pass

class UInv (UnaryOp):
    pass

class UNot (UnaryOp):
    pass
