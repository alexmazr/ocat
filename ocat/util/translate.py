from ..instructions.ast import *
from ..instructions.binaryc import *
from ..instructions.binaryr import *
from ..instructions.unaryr import *
from ..instructions.unaryc import *
from ..instructions.ftype import *
from ..instructions.singlec import *
from ..instructions.singler import *
from ..instructions.jumpr import *
from ..settings import Settings
from .env import Environment

settings = Settings ()

def astTranslation (name, ref, type):
    if name == 'And' and ref == 'r':
        return Andrl if ref == 'r' else Andcl
    return eval (f"{name}{ref}{type[0]}")

astByteMap = {
    (Const, 'rel', 't') : Timeoutcr,
    (Const, 'abs', 't') : Timeoutca,
    (Ref, 'rel', 't') : Timeoutrr,
    (Ref, 'abs', 't') : Timeoutra
}

class OcatIr:
    def __init__(self):
        self.ocat_ir = []
        self.positions = []
        self.byte_pc = 0

    def append (self, instruction):
        self.positions.append (self.byte_pc)
        self.byte_pc += instruction.sizeInBytes
        self.ocat_ir.append (instruction)

    def extend (self, list):
        for instr in list:
            self.append (instr)

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

def translateFetch (node, pc):
    func_ir = []
    if node.timeout is not None:
        # Add timeout instruction
        timeoutType = node.timeout [0]
        timeoutNode = node.timeout [1]
        if isinstance (timeoutNode, Const):
            func_ir.append (astByteMap[(timeoutNode.__class__, timeoutType, 't')] (timeoutNode.value.value))
        else:
            func_ir.append (astByteMap[(timeoutNode.__class__, timeoutType, 't')] (timeoutNode.name))
        pc += func_ir[-1].sizeInBytes
        

    func_ir.append (Fetch (node.args[0].name))
    if len (node.args) > 1:
        # If there is a condition
        func_ir.extend (translate (node.args[1]).ocat_ir)
        func_ir.append (Jmpzr (func_ir[-1].dest, pc))
    return func_ir


def translate (instructions):
    global astByteMap
    env = Environment ()
    ocat_ir = OcatIr ()
    for node in instructions:
        match node:
            case (Declare () | Assign ()):
                type = env.getType (node.name) if isinstance (node, Assign) else node.type
                if isinstance (node.expr, Const):
                    ocat_ir.append (Movc (node.expr.value.value, node.name))
                elif isinstance (node.expr, Ref):
                    ocat_ir.append (Movr (node.expr.name, node.name))
                elif isinstance (node.expr, Timeout):
                    ocat_ir.append (Movr ('tout', node.name))
                elif isinstance (node.expr, Call):
                    id = node.expr.args[0].name
                    if node.expr.name == 'send':
                        ocat_ir.extend (translateSend (node.expr))
                        ocat_ir.append (Movr ('resp', node.name))
                    elif node.expr.name == 'fetch' or node.expr.name == 'fetch_new':
                        ocat_ir.extend (translateFetch (node.expr, ocat_ir.byte_pc))
                        ocat_ir.append (Movr ('resp', node.name))
                    else:
                        raise SystemExit (f"Unknown function '{node.expr.name}': {node.linedata.lineno}, {node.linedata.linepos}")
                elif isinstance (node.expr, BinOp):
                    if isinstance (node.expr.left, Ref):
                        if isinstance (node.expr.right, Ref):
                            ocat_ir.append (astTranslation(node.expr.__class__.__name__, 'r', type) (node.expr.left.name, node.expr.right.name, node.name))
                        else:
                            ocat_ir.append (astTranslation(node.expr.__class__.__name__, 'c', type) (node.expr.right.value.value, node.expr.left.name, node.name))
                    else:
                        ocat_ir.append (astTranslation(node.expr.__class__.__name__, 'c', type) (node.expr.left.value.value, node.expr.right.name, node.name))



                
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