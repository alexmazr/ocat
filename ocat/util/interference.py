from collections import defaultdict

from ..instructions.binaryc import *
from ..instructions.binaryr import *
from ..instructions.unaryc import *
from ..instructions.unaryr import *
from ..instructions.singlec import *
from ..instructions.singler import *
from ..instructions.jumpr import *

# Build the interference graph
#  The goal is to use our liveness analysis and ocat_ir to determine which variables interfere with each other
#  Generally, we look at the current instruction, then we look at the corresponding liveness set after
#  We add an edge between the the variable we write to and the alive variables, unless they are the same, this means the var we write to cannot be assigned to the same register
#   There is an edge case for movr where both registers are the same value, and can thus be assigned the same register


def interference (ocat_ir, liveness_graph):
    interference_graph = defaultdict(lambda: set([]))
    for ir, lg in zip (ocat_ir, reversed (liveness_graph)):
        match ir:
            case Movr ():
                interference_graph [ir.dest] = lg - set ([ir.reg, ir.dest])
            case (BinaryC () | BinaryR () | UnaryC () | UnaryR ()):
                interference_graph [ir.dest] = lg - set ([ir.dest])
            case (SingleC () | SingleR () | JumpR ()):
                pass
    return interference_graph
