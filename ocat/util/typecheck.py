from ..instructions.ast import *
from ..settings import Settings
from .env import Environment

def checkConst (env, settings, assignType, node):
    if assignType == 'float' and node.expr.type != 'float':
        raise SystemExit (f"Invalid assignment to type 'float', '{node.expr.type}': {node.linedata.lineno}, {node.linedata.linepos}")
    elif assignType == 'uint' and node.expr.type != 'uint':
        raise SystemExit (f"Invalid assignment to type 'uint', '{node.expr.type}': {node.linedata.lineno}, {node.linedata.linepos}")
    elif assignType == 'int' and node.expr.type == 'uint':
        # Attempt to cast uint const to int
        try:
            node.expr.value = settings.ocat_int (node.expr.value.value)
            node.expr.type = 'int'
        except:
            raise SystemExit (f"Invalid assignment to type 'int', out of range 'uint': {node.linedata.lineno}, {node.linedata.linepos}")
    elif assignType == 'temp':
        env.updateType (node.name, node.expr.type)
    return node

def checkRef (env, node, assignType, refType):
    if assignType == 'float' and refType != 'float':
        raise SystemExit (f"Invalid assignment to type 'float', '{refType}': {node.linedata.lineno}, {node.linedata.linepos}")
    elif assignType == 'uint' and refType != 'uint':
        raise SystemExit (f"Invalid assignment to type 'uint', '{refType}': {node.linedata.lineno}, {node.linedata.linepos}")
    elif assignType == 'int' and refType != 'uint':
        raise SystemExit (f"Invalid assignment to type 'int', '{refType}': {node.linedata.lineno}, {node.linedata.linepos}")
    elif assignType == 'temp':
        env.updateType (node.name, refType)

def check (instructions):
    env = Environment ()
    settings = Settings ()

    # for node in instructions:
    #     match node:
    #         case (Declare () | Assign ()):
    #             if isinstance (node.expr, Const):
    #                 node.expr = checkConst (env, settings, env.getType (node.name), node)
    #                 continue
        #     case (Declare () | Assign ()):
                # if isinstance (node.expr, Const):
                #     node.expr = checkConst (env, settings, env.getType (node.name), node)
                # # elif isinstance (node.expr, Ref):
                #     checkRef (env, node, env.getType (node.name), env.getType (node.expr.name))
            #     elif isinstance (node.expr, BinOp):
            #         continue
            #         # Get type of left and right, compare them
            #         # See if the type of the assignment is correct
            #     elif isinstance (node.expr, Call):
            #         continue
            #         # Check config for return type of call
            #     elif isinstance (node.expr, UnaryOp):
            #         continue
            #         # Check type of unary against assignment, make sure it makes sense
            #     elif isinstance (node.expr, Cast):
            #         continue
            #         # Once variables have a type set it cannot be changed, make sure that the value of the cast aligns
            # case Call ():
            #     continue
            #     # Type check arguments
            #     # Type check timeout (make sure it is a uint)
            # case For ():
            #     continue
                # Type check the 
    return instructions
