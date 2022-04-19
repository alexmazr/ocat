from ..settings import Settings
settings = Settings ()

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

    def __init__ (self, name, args, linedata, timeout = None):
        self.name = name
        self.args = args
        self.linedata = linedata
        self.timeout = timeout

    def __repr__ (self):
        return f"{type(self).__name__}({self.name}, {self.args}, {self.timeout})"

class Wait:
    isFlat = True

    def __init__ (self, type, time, linedata):
        self.type = type
        self.time = time
        self.linedata = linedata

    def __repr__ (self):
        return f"{type(self).__name__}({self.type}, {self.time})"

class Timeout:
    isFlat = True
    def __init__ (self, linedata):
        self.linedata = linedata

    def __repr__ (self):
        return f"{type(self).__name__}"

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
        self.op = None

    def reduce (self):
        global settings
        if isinstance (self.left, Const) and isinstance (self.right, Const) and self.op is not None:
            try:
                result = eval (f"{self.left.value.value} {self.op} {self.right.value.value}")
                if isinstance (result, float):
                    return Const (settings.ocat_float (result), 'float', None)
                if result >= 0:
                    return Const (settings.ocat_uint (result), 'uint', None)
                else:
                    return Const (settings.ocat_int (result), 'int', None)
            except:
                raise SystemExit (f"'{self.left.value.value} {self.op} {self.right.value.value}' is invalid: {self.linedata.lineno}, {self.linedata.linepos}")
        return self

    def __repr__ (self):
        return f"{type(self).__name__}({self.left}, {self.right})"

class Cast:
    isFlat = False
    
    def __init__ (self, castType, expr, linedata):
        self.castType = castType
        self.expr = expr
        self.linedata = linedata

    def __repr__ (self):
        return f"{type(self).__name__}({self.castType}, {self.expr})"

    def reduce (self):
        global settings
        try:
            if isinstance (self.expr, Const):
                match self.castType:
                    case 'float':
                        return Const (settings.ocat_float (float (self.expr.value.value)), 'float', None)
                    case 'uint':
                        if self.expr.value.value < 0:
                            raise OverflowError
                        return Const (settings.ocat_uint (int (self.expr.value.value)), 'uint', None)
                    case 'int':
                        return Const (settings.ocat_int (int (self.expr.value.value)), 'int', None)
            return self
        except:
            raise SystemExit (f"Cast '{self.expr.value.value}' to '{self.castType}' failed: {self.linedata.lineno}, {self.linedata.linepos}")

class LShift (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '<<'

class RShift (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '>>'

class BitAnd (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '&'

class BitXor (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '^'

class BitOr (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '|'

class Exp (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '**'

class Mod (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '%'

class Add (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '+'

class Sub (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '-'

class Mul (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '*'

class Div (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '/'

class Eq (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '=='

class Neq (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '!='

class And (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = 'and'

class Or (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = 'or'

class Xor (BinOp):
    def reduce (self):
        global settings
        if isinstance (self.left, Const) and isinstance (self.right, Const):
            try:
                result = bool (self.left.value.value) ^ bool (self.right.value.value)
                if isinstance (result, float):
                    return Const (settings.ocat_float (result), 'float', None)
                if result >= 0:
                    return Const (settings.ocat_uint (result), 'uint', None)
                else:
                    return Const (settings.ocat_int (result), 'int', None)
            except:
                raise SystemExit (f"Operation '{type(self).__name__}' will result in over/under flow: {self.linedata.lineno}, {self.linedata.linepos}")
        return self

class Gte (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '>='

class Lte (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '<='

class Lt (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '<'

class Gt (BinOp):
    def __init__ (self, left, right, linedata):
        super ().__init__ (left, right, linedata)
        self.op = '>'
        

class UnaryOp:
    isFlat = False

    def __init__ (self, expr, linedata):
        self.expr = expr
        self.linedata = linedata
        self.op = None
    
    def __repr__ (self):
        return f"{type(self).__name__}({self.expr})"

    def reduce (self):
        global settings
        if isinstance (self.expr, Const):
            try:
                result = eval (f"{self.op} {self.expr.value.value}")
                if isinstance (result, float):
                    return Const (settings.ocat_float (result), 'float', None)
                if result >= 0:
                    return Const (settings.ocat_uint (result), 'uint', None)
                else:
                    return Const (settings.ocat_int (result), 'int', None)
            except:
                raise SystemExit (f"Operation '{type(self).__name__}' will result in over/under flow: {self.linedata.lineno}, {self.linedata.linepos}")
        return self

class USub (UnaryOp):
    def __init__ (self, expr, linedata):
        super ().__init__ (expr, linedata)
        self.op = '-'
        

class UInv (UnaryOp):
    def __init__ (self, expr, linedata):
        super ().__init__ (expr, linedata)
        self.op = '~'
        

class UNot (UnaryOp):
    def __init__ (self, expr, linedata):
        super ().__init__ (expr, linedata)
        self.op = 'not'
        
