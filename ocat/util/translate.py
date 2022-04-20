from ..instructions.ast import *
from ..instructions.binaryc import *
from ..instructions.binaryr import *
from ..instructions.unaryr import *
from ..instructions.unaryc import *
from ..instructions.singlec import *
from ..instructions.singler import *
from ..instructions.jumpr import *
from ..settings import Settings
from .env import Environment

settings = Settings ()

def astTranslation (name, ref, type = ''):
    if name == 'And' and ref == 'r':
        return Andrl if ref == 'r' else Andcl
    if type == '':
        return eval (f"{name}{ref}")
    else:
        return eval (f"{name}{ref}{type[0]}")

astByteMap = {
    (Const, 'rel', 't') : Timeoutcr,
    (Const, 'abs', 't') : Timeoutca,
    (Ref, 'rel', 't') : Timeoutrr,
    (Ref, 'abs', 't') : Timeoutra
}

class OcatIr:
    # Wrapper class for the translated instructions, this is nice because it allows both a 
    #  regular counted list, and also a byte counted list!
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

    def __len__ (self):
        return len (self.ocat_ir)

    def __getitem__ (self, index):
        return self.ocat_ir [index]

def translateSend (node):
    global settings
    func_ir = []

    settingArgs = settings.getCommandArgs (node.args[0].name)
    buffSize = settings.getCommandBufferSize ()
    func_ir.append (Shiftcl (buffSize, 'c0', 'c0'))
    if settingArgs is not None:
        if len (settingArgs) != len (node.args[1:]):
            raise SystemExit (f"Mismatch in number of command arguments, '{len (settingArgs)}' expected '{len (node.args[1:])}' found: {node.linedata.lineno}, {node.linedata.linepos}")
        for index, arg in enumerate (node.args[1:]):
            try:
                argSize = settingArgs [index]
                func_ir.append (Shiftcl (buffSize, 'c1', 'c1'))
            except:
                raise SystemExit (f"Invalid number of command arguments! '{len (settingArgs)}' specified, '{len (node.args) - 1}' found: {node.linedata.lineno}, {node.linedata.linepos}")
            if isinstance (arg, Ref):   
                func_ir.append (Movr (arg.name, 'c1'))
            else:
                func_ir.append (Movc (arg.value.value, 'c1'))
            func_ir.append (Shiftcl (buffSize - argSize, 'c1', 'c1'))
            func_ir.append (Shiftcrl (buffSize - argSize, 'c1', 'c1'))
            func_ir.append (Shiftcl (argSize, 'c0', 'c0'))
            func_ir.append (Orrb ('c0', 'c1', 'c0'))
    elif len (node.args) > 1:
        raise SystemExit (f"Mismatch in number of command arguments, '0' expected '{len (node.args[1:])}' found: {node.linedata.lineno}, {node.linedata.linepos}")
    
    func_ir.append (Send (settings.getCommandId (node.args[0].name)))
    return func_ir

def translateFetch (node, pc, toAssign):
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
        func_ir.append (Fetch (settings.getTelemetryId (node.args[0].name)) if node.name == 'fetch' else FetchN (settings.getTelemetryId (node.args[0].name)))
        func_ir.append (Jmpnzr ('t0', None))
        toutPos = 2
    else:
        func_ir.append (Fetch (settings.getTelemetryId (node.args[0].name)) if node.name == 'fetch' else FetchN (settings.getTelemetryId (node.args[0].name)))

    func_ir.append (Movr ('r1', toAssign))
    if len (node.args) > 1:
        # If there is a condition
        func_ir.extend (translate (node.args[1]).ocat_ir)
        func_ir.append (Jmpzr (func_ir[-1].dest, pc))
    if node.timeout is not None:
        size = sum (instr.sizeInBytes for instr in func_ir)
        func_ir [toutPos].pc = size
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
                    ocat_ir.append (Movr ('t0', node.name))
                elif isinstance (node.expr, Cast):
                    ocat_ir.append (Movr (node.expr.expr.name, node.name))
                elif isinstance (node.expr, Call):
                    if node.expr.name == 'send':
                        ocat_ir.extend (translateSend (node.expr))
                        ocat_ir.append (Movr ('r1', node.name))
                    elif node.expr.name == 'fetch' or node.expr.name == 'fetch_new':
                        ocat_ir.extend (translateFetch (node.expr, ocat_ir.byte_pc, node.name))
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
                elif isinstance (node.expr, UnaryOp):
                    if isinstance (node.expr.expr, Timeout):
                        ocat_ir.append (astTranslation(node.expr.__class__.__name__, 'r') ('t0', node.name))
                    elif isinstance (node.expr.expr, Ref):
                        ocat_ir.append (astTranslation(node.expr.__class__.__name__, 'r') (node.expr.expr.name, node.name))
                else:
                    raise SystemExit (f"Unimplemented node found: {node.expr}")
            case If ():
                # First pull out conditional, assume that the condition is a single ref, otherwise we want to crash
                jumpPc = len (ocat_ir)
                if isinstance (node.condition, Timeout):
                    ocat_ir.append (Jmpzr ('t0', None))
                else:
                    ocat_ir.append (Jmpzr (node.condition.name, None))
                # Add then statements
                ocat_ir.extend (translate (node.then))  
                thenPc = len (ocat_ir)
                ocat_ir.append (Jmpzr ('r0', None))
                # Create jump if conditional fails to else_ section, save the position of the jump at the end of then
                ocat_ir [jumpPc].pc = ocat_ir.byte_pc
                # Add the else_ statement
                ocat_ir.extend (translate (node.else_))
                ocat_ir [thenPc].pc = ocat_ir.byte_pc
            case Call ():
                if node.name == 'send':
                    ocat_ir.extend (translateSend (node))
            case _:
                raise SystemExit (f"Unimplemented node found: {node}")
    return ocat_ir