from ..instructions.binaryc import *
from ..instructions.binaryr import *
from ..instructions.unaryc import *
from ..instructions.unaryr import *
from ..instructions.ftype import *
from ..instructions.singlec import *
from ..instructions.singler import *
from ..instructions.jumpr import *
from .translate import OcatIr


def remove_dead (ocat_asm):
    newAsm = OcatIr ()
    for instr in ocat_asm.ocat_ir:
        match instr:
            case Movr ():
                if instr.reg != instr.dest:
                    newAsm.append (instr)
            case _:
                newAsm.append (instr)
    return newAsm