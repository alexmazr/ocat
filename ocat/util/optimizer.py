from ..ast.nodes import *

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
                if isinstance (node.expr, Const):
                    # If it's a const then we can add it to the env
                    self.opt_env [node.name] = node.expr
                    if not node.mutable:
                        # If this is also immutable then we can remove the declaration
                        return None
                return node
            case Assign ():
                node.expr = self.optimize (node.expr)
                if isinstance (node.expr, Const):
                    # If the assignment is a single const, eliminate it and update the env
                    self.opt_env [node.target] = node.expr
                    return None
                else:
                    # Otherwise attempt to remove the ref from the env, it's value is now unknown
                    self.opt_env.pop (node.target, None)
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






