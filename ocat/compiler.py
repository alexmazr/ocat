from .parser import parser
from .util.env import Environment
from .util.optimize import Optimizer
from .util.flatten import Flattener
from .util.translate import *



import json

def compile (filepath, command_config, telemetry_config):

    env = Environment ()
    
    # Load specified commands and telemetry into environment
    with open (command_config) as cmd_file:
        commands = json.load (cmd_file)
        for name in commands:
            env.push (name, 'cmd', False)
    
    with open (telemetry_config) as tlm_file:
        telemetry = json.load (tlm_file)
        for name in telemetry:
            env.push (name, 'tlm', False)

    with open (filepath) as f:
        print ("\n---------------------ast---------------------")
        ast = parser.parse (f.read () + "\n")
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
        print ("\n---------------------ocat ir---------------------")
        ocat_ir = translate (flat)
        for pc, instr in enumerate (ocat_ir):
            print (pc, end="")
            print (":\t", end="")
            print (instr)
