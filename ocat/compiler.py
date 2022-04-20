from multiprocessing import allow_connection_pickling
from .parser import parser
from .util.optimize import Optimizer
from .util.flatten import Flattener
from .util.typecheck import *
from .util.translate import *
from .util.liveness import *
from .util.interference import *
from .util.allocate import *
from .util.deadremoval import *
from .settings import Settings
import os

def compile (filepath, mission_config, command_config, telemetry_config):

    Settings ().init (mission_config, command_config, telemetry_config)

    with open (filepath) as f:
        print ("\n---------------------ast---------------------")
        ast = parser.parse (os.path.basename (filepath), f.read () + "\n")
        print (ast)
        print ("\n---------------------optimize---------------------")
        optimizer = Optimizer ()
        opt = optimizer.optimize (ast)
        print (opt)
        print ("\n---------------------flat---------------------")
        flattener = Flattener ()
        flat = flattener.flatten (opt)
        for pc, instr in enumerate (flat):
            print (pc, end="")
            print (":\t", end="")
            print (instr)
        print ("\n---------------------type check---------------------")
        checked = check (flat)
        for pc, instr in enumerate (checked):
            print (pc, end="")
            print (":\t", end="")
            print (instr)
        print ("\n---------------------ocat ir---------------------")
        ocat_ir = translate (checked)
        for instr, pc in zip (ocat_ir.ocat_ir, ocat_ir.positions):
            print (pc, end="")
            print (":\t", end="")
            print (instr)
        print (f"Length: {ocat_ir.byte_pc}")

        print ("\n---------------------liveness---------------------")
        liveness_graph = liveness (ocat_ir.ocat_ir)
        for instr, alive in zip (ocat_ir.ocat_ir, reversed (liveness_graph)):
            print (instr)
            print (alive)

        print ("\n---------------------interference---------------------")
        ig = interference (ocat_ir.ocat_ir, liveness_graph)
        for k,v in ig.items ():
            print (f"{k}: {v}")

        print ("\n---------------------First Form Byte Code---------------------")
        ocat_asm = allocate (ig, ocat_ir)
        for instr, pc in zip (ocat_asm.ocat_ir, ocat_ir.positions):
            print (pc, end="")
            print (":\t", end="")
            print (instr)
        print (f"Length: {ocat_asm.byte_pc}")

        print ("\n---------------------Final Byte Code---------------------")
        ocat_asm = remove_dead (ocat_asm)
        for instr, pc in zip (ocat_asm.ocat_ir, ocat_ir.positions):
            print (pc, end="")
            print (":\t", end="")
            print (instr)
        print (f"Length: {ocat_asm.byte_pc}")

        binary = bytearray ()
        for instr in ocat_asm.ocat_ir:
            instr.setFields ()
            binary.extend (instr.pack ())
        
        with open('out.bin', 'wb') as writer:
            writer.write (binary)