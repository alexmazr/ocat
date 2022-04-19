from ..instructions.ast import *
from ..settings import Settings
from .env import Environment

def checkConst (env, settings, const, assignType, assignName):
    if assignType == 'temp':
        env.updateType (assignName, const.type)
    elif assignType == 'int' and const.type == 'uint':
        # Attempt to cast down uint const to int, this is the only implicit cast allowed
        try:
            const.value = settings.ocat_int (const.value.value)
            const.type = 'int'
        except:
            raise SystemExit (f"Invalid bassignment to type 'int', out of range 'uint': {const.linedata.lineno}, {const.linedata.linepos}")
    elif assignType != const.type:
        raise SystemExit (f"Invalid assignment to type '{assignType}', '{const.type}': {const.linedata.lineno}, {const.linedata.linepos}")
    return const

def checkRef (env, node, assignType, refType):
    if assignType == 'temp':
        # The first assignment to a temp will decide it's type, after that it cannot change
        env.updateType (node.name, refType)
    elif assignType != refType:
        raise SystemExit (f"Invalid assignment to type '{assignType}', '{refType}': {node.linedata.lineno}, {node.linedata.linepos}")

def checkBinOp (env, settings, node, assignType, assignName):
    # Assume all references have a concrete type and note reference types cannot change after they are set!
    if isinstance (node.left, Const):
        # node right is the ref, make sure the left const matches it's type
        refType = env.getType (node.right.name)
        node.left = checkConst (env, settings, node.left, refType, assignName)
    elif isinstance (node.right, Const):
        # node left is the ref, make sure the right const matches it's type
        refType = env.getType (node.left.name)
        node.right = checkConst (env, settings, node.right, refType, assignName)
    else:
        # node.left and node.right are ref, make sure they match each other's type
        refType = env.getType (node.left.name)
        rightType = env.getType (node.right.name)
        if refType != rightType:
            raise SystemExit (f"Invalid dassignment to type '{refType}', '{rightType}': {node.linedata.lineno}, {node.linedata.linepos}")
    if assignType == 'temp':
        # The first assignment to a temp will decide it's type, after that it cannot change
        env.updateType (assignName, refType)
    elif refType != assignType:
        print (node)
        raise SystemExit (f"Invalid assignment to type '{assignType}', '{refType}': {node.linedata.lineno}, {node.linedata.linepos}")
    return node

def check (instructions):
    env = Environment ()
    settings = Settings ()

    for node in instructions:
        match node:
            case (Declare () | Assign ()):
                match node.expr:
                    case Const () as const:
                        const = checkConst (env, settings, const, env.getType (node.name), node.name)
                    case Ref () as ref:
                        checkRef (env, ref, env.getType (node.name), env.getType (ref.name))
                    case BinOp () as binop:
                        binop = checkBinOp (env, settings, binop, env.getType (node.name), node.name)
                    case Cast () as cast:
                        checkRef (env, node, env.getType (node.name), cast.castType)
                    case Call () as call if call.name == 'fetch' or call.name == 'fetch_new':
                        assignType = env.getType (node.name)
                        tlmType = env.getType (call.args [0].name)
                        if assignType != tlmType:
                            raise SystemExit (f"Invalid assignment to type '{assignType}', '{tlmType}': {node.linedata.lineno}, {node.linedata.linepos}")

                        if len (call.args) > 1:
                            call.args [1] = check (call.args [1])

                            timeoutType = env.getType (call.timeout [1].name) if isinstance (call.timeout [1], Ref) else call.timeout [1].type
                            if timeoutType != 'uint':
                                raise SystemExit (f"Invalid timeout type '{timeoutType}': {node.linedata.lineno}, {node.linedata.linepos}")
                    
                                

    return instructions
