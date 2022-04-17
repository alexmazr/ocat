from .env import Environment
from ..ast.nodes import *

class Optimizer:
    def __init__ (self, mode = "default"):
        self.env = Environment ()
        self.mode = mode

    def isRefAndConst (self, ref):
        if isinstance (ref, Ref) and isinstance (self.env.peek (ref.name), Const):
            return True
        return False

    def optimize (self, instructions):
        print (f"Optimizing in '{self.mode}' mode")
        instr_opt = []
        i = 0
        while i < len (instructions):
            instr = instructions [i]
            match instr:
                case Assign () as node:
                    match node.expr:
                        case BinOp () as toReduce:
                            if self.mode == "default":
                                if self.isRefAndConst (toReduce.left):
                                    toReduce.left = self.env.peek (toReduce.left.name)
                                if self.isRefAndConst (toReduce.right):
                                    toReduce.right = self.env.peek (toReduce.right.name)
                                node.expr = toReduce.reduce ()
                    if isinstance (node.expr, Const):
                        self.env.makeConst (node.target, node.expr)
                    elif isinstance (node.expr, Ref) and isinstance (self.env.peek (node.expr.name), Const):
                        node.expr = self.env.peek (node.expr.name)
                        instr_opt.append (node)
                    else:
                        instr_opt.append (node)
                case Declare () as node:
                    if isinstance (node.expr, Const):
                        self.env.makeConst (node.name, node.expr)
                    elif isinstance (node.expr, Ref) and isinstance (self.env.peek (node.expr.name), Const):
                        node.expr = self.env.peek (node.expr.name)
                        self.env.makeConst (node.name, node.expr)
                    instr_opt.append (node)
                case _ as node:
                    instr_opt.append (node)
            i += 1
        offset = len (instructions) - len (instr_opt) 
        for node in instr_opt:
            if isinstance (node, Jump):
                node.pc -= offset
        return instr_opt





