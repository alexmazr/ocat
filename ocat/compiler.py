from .parser import parser
from .util.optimize import Optimizer
from .util.flatten import Flattener
from .util.typecheck import *
from .util.translate import *
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
