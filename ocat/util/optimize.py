from ..instructions.ast import *
import copy

class Optimizer:
    def __init__ (self):
        self.opt_env = {}

    def optimizeList (self, statements):
        ret = []
        for stmt in statements:
            ostmt = self.optimize (stmt)
            if ostmt is not None:
                ret.append (ostmt)
        return ret

    def optimize (self, node):
        match node:
            case Program ():
                node.statements = self.optimizeList (node.statements)
                return node
            case EndProgram ():
                node.args = self.optimizeList (node.args)
                return node
            case Declare ():
                node.expr = self.optimize (node.expr)
                if isinstance (node.expr, Const) or isinstance (node.expr, Ref):
                    # If it's immutable, and being declared with a const or ref, remove it.
                    self.opt_env [node.name] = node.expr
                    if not node.mutable:
                        return None
                return node
            case Assign ():
                node.expr = self.optimize (node.expr)
                if isinstance (node.expr, Const) or isinstance (node.expr, Ref):
                    # If the assignment is a single const, eliminate it and update the env
                    self.opt_env [node.name] = node.expr
                    return None
                else:
                    # Otherwise attempt to remove the ref from the env, it's value is now unknown
                    self.opt_env.pop (node.name, None)
                return node
            case Call ():
                node.args = self.optimizeList (node.args)
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
                # For loops clear our assumptions about data, so clear the env
                self.opt_env = {}
                node.statements = self.optimizeList (node.statements)
                return node
            case Wait ():
                node.time = self.optimize (node.time)
                return node
            case BinOp ():
                node.left = self.optimize (node.left)
                node.right = self.optimize (node.right)
                return node.reduce ()
            case Const ():
                 return node
            case Ref ():
                return self.opt_env.get (node.name, node)
            case _ :
                return node






