from ..settings import Settings

from ..instructions.binaryc import *
from ..instructions.binaryr import *
from ..instructions.unaryc import *
from ..instructions.unaryr import *
from ..instructions.ftype import *
from ..instructions.singlec import *
from ..instructions.singler import *
from ..instructions.jumpr import *


settings = Settings ()
static_reg = set (['c0', 'c1', 't0', 'r0', 'r1']) # These registers are only assigned during translate, and can be ignore in our interference graph


def allocate (ig, ocat_ir):
    registers = [f"r{num}" for num in range (2, settings.getNumRegisters ())]
    settings.warnPotentialUnusedMemory (len (registers) + 2)
    user_vars = {key : val - static_reg for key, val in ig.items () if key not in static_reg}
    assignments = {}
    while user_vars:
        most_saturated = max (user_vars, key=lambda k: len (user_vars [k]))

        # Attempt to assign the variable a register
        color = ''
        for register in registers:
            if register not in user_vars [most_saturated]: 
                assignments [most_saturated] = register
                color = register
                break
        else:
            raise SystemExit (f"This program uses too many registers, increase mission memory size or decrease program variable usage.")
        
        # Cascade the register allocation through the user_vars
        for name in user_vars [most_saturated]:
            if name in user_vars:
                user_vars [name].discard (most_saturated)
                user_vars [name].add (color)

        # Remove this from our user_vars, we have colored it, and we shouldn't see it again
        del user_vars [most_saturated]

    for instr in ocat_ir.ocat_ir:
        match instr:
            case BinaryR ():
                instr.left = assignments.get (instr.left, instr.left)
                instr.right = assignments.get (instr.right, instr.right)
                instr.dest = assignments.get (instr.dest, instr.dest)
            case BinaryC ():
                instr.right = assignments.get (instr.right, instr.right)
                instr.dest = assignments.get (instr.dest, instr.dest)
            case UnaryC ():
                instr.dest = assignments.get (instr.dest, instr.dest)
            case UnaryR ():
                instr.reg = assignments.get (instr.reg, instr.reg)
                instr.dest = assignments.get (instr.dest, instr.dest)
            case (SingleR () | JumpR ()):
                instr.reg = assignments.get (instr.reg, instr.reg)
            case (FType () | SingleC ()):
                pass

    return ocat_ir
    
        
    

