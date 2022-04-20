from ..instructions.binaryc import *
from ..instructions.binaryr import *
from ..instructions.unaryc import *
from ..instructions.unaryr import *
from ..instructions.ftype import *
from ..instructions.singlec import *
from ..instructions.singler import *
from ..instructions.jumpr import *

# Liveness is a graph with nodes that preside between instructions, and the instructions create the edges
# Start the end, with an empty set
#  Look at instructions
#  Remove the variable that the instruction writes to
#  Add any variables that are read by the instruction

# livesness_set.remove (reg_write)
# liveness_set.add (reg_read's)

def liveness (ocat_ir):
    liveness_set = set([])
    liveness_graph = [liveness_set]
    for ir in reversed (ocat_ir):
        match ir:
            case BinaryC ():
                liveness_set.discard (ir.dest)
                liveness_set.add (ir.right)
                liveness_graph.append (liveness_set.copy ())
            case BinaryR ():
                liveness_set.discard (ir.dest)
                liveness_set.add (ir.left)
                liveness_set.add (ir.right)
                liveness_graph.append (liveness_set.copy ())
            case FType ():
                liveness_graph.append (liveness_set.copy ())
            case SingleC ():
                liveness_graph.append (liveness_set.copy ())
            case SingleR ():
                liveness_set.add (ir.reg)
                liveness_graph.append (liveness_set.copy ())
            case UnaryC ():
                liveness_set.discard (ir.dest)
                liveness_graph.append (liveness_set.copy ())
            case UnaryR ():
                liveness_set.discard (ir.dest)
                liveness_set.add (ir.reg)
                liveness_graph.append (liveness_set.copy ())
            case JumpR ():
                liveness_set.add (ir.reg)
                liveness_graph.append (liveness_set.copy ())
    return liveness_graph
