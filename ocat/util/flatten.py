from ..instructions.ast import *
from .env import Environment

class Flattener:
    def __init__ (self):
        self.tempId = 0
        self.instructions = []
        self.env = Environment ()

    # All temp generation must go through this function, guarantees addition to variable environment
    def getTemp (self):
        self.tempId += 1
        tempStr = f"t-{self.tempId}"
        self.env.push (tempStr, 'temp', False)
        return tempStr

    # Uses node class field to determine if this node is flat
    #  A flat node is either a const of a ref, all other nodes become
    #  a ref to a temp variable. An Assign for each temp is also created.
    def checkFlat (self, node):
        if node.isFlat == False:
            temp = self.getTemp ()
            self.instructions.append (Assign (temp, node, node.linedata))
            return Ref (temp, None)
        return node

    def flatten (self, node):
        match node:
            case Program ():
                for stmt in node.statements:
                    self.instructions.append (self.flatten (stmt))
                self.instructions = [instr for instr in self.instructions if instr is not None]
                return self.instructions
            case EndProgram ():
                return node
            case Declare ():
                if node.expr is not None:
                    node.expr =  self.flatten (node.expr)
                    self.env.push (node.name, node.type, node.mutable)
                return node
            case Assign ():
                if node.name not in self.env or not self.env.peek (node.name).mutable:
                    raise SystemExit (f"Invalid assignment on '{node.name}': {node.linedata.lineno}, {node.linedata.linepos}")
                node.expr = self.flatten (node.expr)
                return node
            case Call ():
                match node.name:
                    case 'send':
                        node.args = [self.checkFlat (self.flatten (expr)) for expr in node.args]
                    case ('fetch' | 'fetch_all') if len (node.args) >= 2:
                        jumpPc = len (self.instructions)
                        self.instructions.append (Jump (None))
                        condition = self.checkFlat (self.flatten (node.args[1]))
                        if len (node.args) == 3:
                            self.instructions.append (self.checkFlat (self.flatten (node.args[2])))
                            node.args.pop ()
                        self.instructions.append (Ret (condition))
                        node.args[1] = Exec (jumpPc + 1)
                        self.instructions [jumpPc].pc = len (self.instructions)
                return node
            case IfExpr ():
                node.condition = self.checkFlat (self.flatten (node.condition))

                condPc = len (self.instructions)
                self.instructions.append (Jump (None))

                thenPc = len (self.instructions)
                node.then = self.checkFlat (self.flatten (node.then))
                self.instructions.append (Ret (node.then))
                
                elsePc = len (self.instructions)
                node.else_ = self.checkFlat (self.flatten (node.else_))
                self.instructions.append (Ret (node.else_))

                self.instructions [condPc].pc = len (self.instructions)
                node.then = Exec (thenPc)
                node.else_ = Exec (elsePc)
                return node
            case If ():
                node.condition = self.checkFlat (self.flatten (node.condition))
                if isinstance (node.condition, Const) and node.condition:
                    [self.instructions.append (self.flatten (then)) for then in node.then]
                elif isinstance (node.condition, Const) and not node.condition:
                    [self.instructions.append (self.flatten (else_)) for then in node.else_]
                else:
                    node.then = [self.flatten (then) for then in node.then]
                    node.else_ = [self.flatten (else_) for else_ in node.else_]
                    return node
            case For ():
                self.env.push (node.iterator, 'itr', False)
                node.args = [self.flatten (expr) for expr in node.args]
                node.statements = [stmt for stmt in node.statements]
                return node
            case Wait ():
                node.time = self.checkFlat (self.flatten (node.time))
                return node
            case BinOp ():
                node.left = self.checkFlat (self.flatten (node.left))
                node.right = self.checkFlat (self.flatten (node.right))
                return node
            case UnaryOp ():
                node.expr = self.checkFlat (self.flatten (node.expr))
                return node
            case Const ():
                return node
            case Ref ():
                if node.name not in self.env:
                    print (f"Unknown reference '{node.name}': {node.linedata.lineno}, {node.linedata.linepos}")
                    print ("Dumping known references:")
                    self.env.dump ()
                    raise SystemExit ()
                return node

