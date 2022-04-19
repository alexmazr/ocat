from ..instructions.ast import *

class Optimizer:
    def __init__ (self):
        self.opt_env = {}
        self.declared = set([])

    def optimizeList (self, statements):
        ret = []
        for stmt in statements:
            ostmt = self.optimize (stmt)
            if ostmt is not None:
                ret.append (ostmt)
        return ret

    # Also perform declaration checks
    def optimize (self, node):
        match node:
            case Program ():
                node.statements = self.optimizeList (node.statements)
                return node
            case EndProgram ():
                node.args = self.optimizeList (node.args)
                return node
            case Declare ():
                if node.name in self.declared:
                    raise SystemExit (f"Variable '{node.name}' previous declared: {node.linedata.lineno}, {node.linedata.linepos}")
                else:
                    self.declared.add (node.name)
                node.expr = self.optimize (node.expr)
                if not node.mutable and isinstance (node.expr, Const) or isinstance (node.expr, Ref):
                    # If it's immutable, and being declared with a const or ref, remove it.
                    self.opt_env [node.name] = node.expr
                    return None
                return node
            case Assign ():
                node.expr = self.optimize (node.expr)
                return node
            case Call ():
                node.args = self.optimizeList (node.args)
                if node.timeout is not None:
                    node.timeout = (node.timeout[0], self.optimize (node.timeout[1]))
                return node
            case IfExpr ():
                node.condition = self.optimize (node.condition)
                if isinstance (node.condition, Const):
                    return self.optimize (node.then) if node.condition.value else self.optimize (node.else_)
                node.then = self.optimize (node.then)
                node.else_ = self.optimize (node.else_)
                return node
            case If ():
                node.condition = self.optimize (node.condition)
                node.then = self.optimizeList (node.then)
                node.else_ = self.optimizeList (node.else_)
                return node
            case For ():
                node.args = self.optimizeList (node.args)
                node.statements = self.optimizeList (node.statements)
                return node
            case Wait ():
                node.time = self.optimize (node.time)
                return node
            case BinOp ():
                node.left = self.optimize (node.left)
                node.right = self.optimize (node.right)
                return node.reduce ()
            case Cast ():
                node.expr = self.optimize (node.expr)
                return node.reduce ()
            case Const ():
                 return node
            case Ref ():
                return self.opt_env.get (node.name, node)
            case _ :
                return node






