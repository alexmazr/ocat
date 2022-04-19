from ..instructions.ast import *
from ..settings import Settings
from .env import Environment

class Flattener:
    def __init__ (self):
        self.tempId = 0
        self.instructions = []
        self.env = Environment ()
        self.settings = Settings ()

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
            return Ref (temp, node.linedata)
        return node

    def flattenFetch (self, node):
        if len (node.args) == 1:
            return node
        elif len (node.args) == 2:
            argPc = len (self.instructions)
            temp = self.checkFlat (self.flatten (node.args[1]))
            node.args [1] = self.instructions [argPc:]
            self.instructions = self.instructions [:argPc]
            if len (node.args [1]) == 0:
                if isinstance (temp, Const) and temp.value.value:
                    node.args.pop ()
                else:
                    node.args [1] = [Assign (self.getTemp (), temp, node.linedata)]       
        else:
            raise SystemExit (f"Invalid number of args in '{node.name}', '{len(node.args)}' found, must be less than 3: {node.linedata.lineno}, {node.linedata.linepos}")
        
        if node.timeout is not None:
            node.timeout = (node.timeout[0], self.checkFlat (self.flatten (node.timeout[1])))
        return node

    def checkCommandOrTelemetry (self, node):
        if node.name == 'send': 
            if not isinstance (node.args[0], Ref):
                raise SystemExit (f"Command must be a name: {node.linedata.lineno}, {node.linedata.linepos}")
            if not isinstance (node.args[0], Ref) or not self.settings.commandDefined (node.args [0].name):
                raise SystemExit (f"Command '{node.args[0].name}' not defined: {node.linedata.lineno}, {node.linedata.linepos}")
            else:
                self.env.push (node.args[0].name, 'command', False)
        elif node.name == 'fetch' or node.name == 'fetch_new':
            if not isinstance (node.args[0], Ref):
                raise SystemExit (f"Telemetry must be a name: {node.linedata.lineno}, {node.linedata.linepos}")
            if not self.settings.telemetryDefined (node.args [0].name):
                raise SystemExit (f"Telemtry '{node.args[0].name}' not defined: {node.linedata.lineno}, {node.linedata.linepos}")
            else:
                self.env.push (node.args[0].name, self.settings.getTelemetryType (node.args[0].name), False)
        
    def flatten (self, node):
        match node:
            case Program ():
                for stmt in node.statements:
                    # TODO: Figure out why python behaves differently if you append self.flatten (stmt) directly if self.instructions get mutated during call
                    flat = self.flatten (stmt)
                    self.instructions.append (flat)
                self.instructions = [instr for instr in self.instructions if instr is not None]
                return self.instructions
            case EndProgram ():
                return node
            case Declare ():
                if node.expr is not None:
                    node.expr = self.flatten (node.expr)
                    self.env.push (node.name, node.type, node.mutable)
                return node
            case Assign ():
                if node.name not in self.env:
                    raise SystemExit (f"Variable '{node.name}' assigned before declaration: {node.linedata.lineno}, {node.linedata.linepos}")
                if not self.env.peek (node.name).mutable:
                    raise SystemExit (f"Invalid assignment on '{node.name}', must be tagged mut: {node.linedata.lineno}, {node.linedata.linepos}")
                node.expr = self.flatten (node.expr)
                return node
            case Call ():
                if len (node.args) == 0:
                    SystemExit (f"Invalid number of args in '{node.name}', '0' found, must be at least 1: {node.linedata.lineno}, {node.linedata.linepos}")
                else:
                    self.checkCommandOrTelemetry (node)
                if node.name == 'fetch' or node.name == 'fetch_new':
                    node = self.flattenFetch (node)
                else:
                    node.args = [self.checkFlat (self.flatten (expr)) for expr in node.args]
                return node
            # case IfExpr ():
            #     node.condition = self.checkFlat (self.flatten (node.condition))
            #     temp = self.getTemp ()
            #     thenPc = len (self.instructions)
            #     for stmt in node.then:
            #         self.checkFlat (self.flatten (stmt))
            #     node.then = self.instructions [thenPc:]
            #     print (node)
            #     node.then.append (Assign (temp, Ref (node.then[-1].name, node.linedata), node.linedata))
            #     self.instructions = self.instructions [:thenPc]

            #     elsePc = len (self.instructions)
            #     for stmt in node.else_:
            #         self.checkFlat (self.flatten (stmt))
            #     node.else_ = self.instructions [elsePc:]

            #     self.instructions = self.instructions [:elsePc]
            #     return node
            case If ():
                node.condition = self.checkFlat (self.flatten (node.condition))
                if isinstance (node.condition, Const) and node.condition.value.value:
                    [self.instructions.append (self.flatten (then)) for then in node.then]
                elif isinstance (node.condition, Const) and not node.condition.value.value:
                    [self.instructions.append (self.flatten (else_)) for else_ in node.else_]
                else:
                    thenPc = len (self.instructions)
                    for stmt in node.then:
                        flat = self.flatten (stmt)
                        self.instructions.append (flat)
                    node.then = self.instructions [thenPc:]
                    self.instructions = self.instructions [:thenPc]

                    elsePc = len (self.instructions)
                    for stmt in node.else_:
                        flat = self.flatten (stmt)
                        self.instructions.append (flat)
                    node.else_ = self.instructions [elsePc:]

                    self.instructions = self.instructions [:elsePc]
                    return node
            case For ():
                self.env.push (node.iterator, 'itr', False)
                node.args = [self.checkFlat (self.flatten (expr)) for expr in node.args]
                stmtPc = len (self.instructions)
                for stmt in node.statements:
                    flat = self.flatten (stmt)
                    self.instructions.append (flat)
                node.statements = self.instructions [stmtPc:]
                self.instructions = self.instructions [:stmtPc]
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
            case Cast ():
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
            case _:
                return node

