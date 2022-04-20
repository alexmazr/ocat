from ctypes import *
import json

commands = {}
telemetry = {}
mission = {}

class Settings:
    def __init__ (self):
        pass
        
    def init (self, mission_config, command_config, telemetry_config):
        global commands, telemetry, mission

        with open (mission_config) as mission_file:
            mission = json.load (mission_file)
            if 'register_size' not in mission:
                raise SystemExit ("ERROR: Register size in mission configuration not specified!")

        with open (command_config) as cmd_file:
            commands = json.load (cmd_file)
        
        with open (telemetry_config) as tlm_file:
            telemetry = json.load (tlm_file)

    def commandDefined (self, name):
        global commands
        return name in commands 

    def getCommandArgs (self, name):
        global commands
        return commands [name]

    def getCommandBufferSize (self):
        global mission
        return mission ['command_buffer']
    
    def telemetryDefined (self, name):
        global telemetry
        return name in telemetry

    def getTelemetryType (self, name):
        global telemetry
        return telemetry [name]

    def getNumRegisters (self):
        global mission
        return int ((mission ['memory_size'] - (mission ['command_buffer'] * 2) - 1) / mission ['register_size'])        

    def warnPotentialUnusedMemory (self, numr):
        global memory
        mem_used = ((numr * mission ['register_size']) + (mission ['command_buffer'] * 2) + 1)
        if mission ['memory_size'] > mem_used:
            print (f"WARNING: Allowed mem {mission ['memory_size']} is greater than potential mem used {mem_used}")

    def ocat_float (self, val):
        global mission
        match mission ['register_size']:
            case 32:
                return c_float (val)
            case 64:
                return c_double (val)
            case _:
                raise SystemExit (f"float not supported for register size '{mission ['register_size']}")

    def ocat_int (self, val):
        global mission
        if val >= (2 ** (mission['register_size'] - 1)) or val < -(2 ** (mission['register_size'] - 1)):
            raise OverflowError
        match mission ['register_size']:
            case 8:
                return c_int8 (val)
            case 16:
                return c_int16 (val)
            case 32:
                return c_int32 (val)
            case 64:
                return c_int64 (val)
            case _:
                raise SystemExit (f"int not supported for register size '{mission ['register_size']}")
    
    def ocat_uint (self, val):
        global mission
        if val >= (2 ** mission['register_size']):
            raise OverflowError
        match mission ['register_size']:
            case 8:
                return c_uint8 (val)
            case 16:
                return c_uint16 (val)
            case 32:
                return c_uint32 (val)
            case 64:
                return c_uint64 (val)
            case _:
                raise SystemExit (f"uint not supported for register size '{mission ['register_size']}")