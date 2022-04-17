from pickletools import optimize
from .parser import parser
from .util.flattener import Flattener
from .util.env import Environment
from .util.optimizer import Optimizer
import os

import json

def compile (filepath, command_config, telemetry_config):

    env = Environment ()
    print (os.getcwd())
    
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
        print ("\n---------------------flat---------------------")
        flattener = Flattener ()
        flat = flattener.flatten (ast)
        for pc, instr in enumerate (flat):
            print (pc, end="")
            print (":\t", end="")
            print (instr)
        print ("\nEnvironment after flattening:")
        env.dump ()
        print ("\n---------------------optimized---------------------")
        optimizer = Optimizer ()
        opt = optimizer.optimize (flat)
        for pc, instr in enumerate (opt):
            print (pc, end="")
            print (":\t", end="")
            print (instr)
    