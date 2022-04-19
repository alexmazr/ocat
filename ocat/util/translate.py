from ..instructions.ast import *
from ..instructions.binaryc import *
from ..instructions.binaryr import *
from ..instructions.unaryr import *
from ..instructions.unaryc import *
from ..instructions.ftype import *
from ..instructions.singlec import *
from ..settings import Settings
from .env import Environment

settings = Settings ()

astByteMap = {
    (Add, 'uint', 'r') : Addru,
    (Add, 'int', 'r') : Addri,
    (Add, 'float', 'r') : Addrf,
    (Add, 'uint', 'c') : Addcu,
    (Add, 'int', 'c') : Addci,
    (Add, 'float', 'c') : Addcf
}

def translateSend (node):
    global settings
    func_ir = []
    settingArgs = settings.getCommandArgs (node.args[0].name)
    buffSize = settings.getCommandBufferSize ()
    func_ir.append (Shiftcl (buffSize, 'c1', 'c1'))
    for index, arg in enumerate (node.args[1:]):
        try:
            argSize = settingArgs [index]
        except:
            raise SystemExit (f"Invalid number of command arguments! '{len (settingArgs)}' specified, '{len (node.args) - 1}' found: {node.linedata.lineno}, {node.linedata.linepos}")
        if isinstance (arg, Ref):   
            func_ir.append (Movr (arg.name, 'c2'))
        else:
            func_ir.append (Movc (arg.value.value, 'c2'))
        func_ir.append (Shiftcl (buffSize - argSize, 'c2', 'c2'))
        func_ir.append (Shiftcr (buffSize - argSize, 'c2', 'c2'))
        func_ir.append (Shiftcl (argSize, 'c1', 'c1'))
        func_ir.append (Orrb ('c1', 'c2', 'c1'))
    func_ir.append (Movr ('c2', 'c1'))
    func_ir.append (Send ())
    return func_ir

# def translateFetch (node):
#     func_ir = []
#     if node.time is not None:


def translate (instructions):
    global astByteMap
    env = Environment ()
    ocat_ir = []
    for node in instructions:
        match node:
            case (Declare () | Assign ()):
                type = env.getType (node.name) if isinstance (node, Assign) else node.type
                if isinstance (node.expr, Const):
                    ocat_ir.append (Movc (node.expr.value.value, node.name))
                elif isinstance (node.expr, Ref):
                    ocat_ir.append (Movr (node.expr.name, node.name))
                elif isinstance (node.expr, Call):
                    id = node.expr.args[0].name
                    if node.expr.name == 'send':
                        ocat_ir.extend (translateSend (node.expr))
                        ocat_ir.append (Movr ('resp', node.name))
                    elif node.expr.name == 'fetch':
                        ocat_ir.append (Fetch (id))
                        ocat_ir.append (Movr ('resp', node.name))
                    elif node.expr.name == 'fetch_new':
                        ocat_ir.append (FetchN (id))
                        ocat_ir.append (Movr ('resp', node.name))
                    else:
                        raise SystemExit (f"Unknown function '{node.expr.name}': {node.linedata.lineno}, {node.linedata.linepos}")
                elif isinstance (node.expr, BinOp):
                    if isinstance (node.expr.left, Ref):
                        if isinstance (node.expr.right, Ref):
                            ocat_ir.append (astByteMap[(node.expr.__class__, type, 'r')] (node.expr.left.name, node.expr.right.name, node.name))
                        else:
                            ocat_ir.append (astByteMap[(node.expr.__class__, type, 'c')] (node.expr.right.value.value, node.expr.left.name, node.name))
                    else:
                        ocat_ir.append (astByteMap[(node.expr.__class__, type, 'c')] (node.expr.left.value.value, node.expr.right.name, node.name))

                
                # elif isinstance (node.expr, Add) and node.type :
                #     if isinstance (node.expr.left, Ref):
                #         if isinstance (node.expr.right, Ref):
                #             ocat_ir.append (Addr (node.expr.left.name, node.expr.right.name, node.name))
                #         else:
                #             ocat_ir.append (Addc (node.expr.right.value, node.expr.left.name, node.name))
                #     else:
                #         ocat_ir.append (Addc (node.expr.left.value, node.expr.right.name, node.name))
            case Call ():
                if node.name == 'send':
                    ocat_ir.extend (translateSend (node))
            case _:
                ocat_ir.append (node)
    return ocat_ir