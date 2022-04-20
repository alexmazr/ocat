from ctypes import *
from socket import timeout
from .instructions.bytecode import BinaryR
from .instructions.bytecode import UnaryR
from .instructions.bytecode import BinaryC
from .instructions.bytecode import UnaryC
from .instructions.bytecode import SingleC
from .instructions.bytecode import SingleR
from .instructions.bytecode import JumpR
from timeit import default_timer as timer

command_registers = [0,0]
timeout_flag = 0
timeout_set = False
timeout_value = 0
timestamp = 0
registers = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

class Runtime:
    def __init__ (self, filename):
        with open (filename) as f:
            self.binary = f.read ()
        self.length = int (len (self.binary))
        self.pc = 0
        self.offset = 0

        # print (BinaryR.sizeInBits)
        # print (UnaryR.sizeInBits)
        # print (BinaryC.sizeInBits)
        # print (UnaryC.sizeInBits)
        # print (SingleC.sizeInBits)
        # print (SingleR.sizeInBits)
        # print (JumpR.sizeInBits)

    def readChunk (self, size):
        ret = int (self.binary [self.offset:self.offset + size], 2)
        self.offset += size
        return ret

    def dumpReg (self):
        global registers
        print (registers)

    def decode (self):
        if self.pc >= self.length:
            raise SystemExit (f"Program finished.")
        instrType = self.readChunk (3)
        opcode = self.readChunk (6)
        match instrType:
            case 0:
                lRegType = self.readChunk (2)
                lReg = self.readChunk (4)
                rRegType = self.readChunk (2)
                rReg = self.readChunk (4)
                dRegType = self.readChunk (2)
                dReg = self.readChunk (4)
                self.readChunk (5)
                dispatcher [(instrType, opcode)] (lRegType, lReg, rRegType, rReg, dRegType, dReg)
            case 1:
                srcRegType = self.readChunk (2)
                srcReg = self.readChunk (4)
                destRegType = self.readChunk (2)
                destReg = self.readChunk (4)
                self.readChunk (3)
                dispatcher [(instrType, opcode)] (srcRegType, srcReg, destRegType, destReg)
            case 2:
                const = self.readChunk (32)
                srcRegType = self.readChunk (2)
                srcReg = self.readChunk (4)
                destRegType = self.readChunk (2)
                destReg = self.readChunk (4)
                self.readChunk (3)
                dispatcher [(instrType, opcode)] (const, srcRegType, srcReg, destRegType, destReg)
            case 3:
                const = self.readChunk (32)
                regType = self.readChunk (2)
                reg = self.readChunk (4)
                self.readChunk (1)
                dispatcher [(instrType, opcode)] (const, regType, reg)
            case 4:
                const = self.readChunk (32)
                self.readChunk (7)
                dispatcher [(instrType, opcode)] (const)
            case 5:
                regType = self.readChunk (2)
                reg = self.readChunk (4)
                self.readChunk (1)
                dispatcher [(instrType, opcode)] ()
            case 6:
                regType = self.readChunk (2)
                reg = self.readChunk (4)
                jDest = self.readChunk (16)
                self.readChunk (1)
                self.pc = dispatcher [(instrType, opcode)] (regType, reg, jDest, self.offset)
                self.offset = self.pc
                return
            case _:
                raise SystemExit (f"unknown type: {instrType}, {opcode}")
        self.pc = self.offset
        

def readReg (regType, reg):
    global registers, command_registers, timeout_flag
    if regType == 0:
        return command_registers [reg]
    elif regType == 1:
        return timeout_flag
    elif regType == 2:
        return registers [reg]

def writeReg (regType, reg, value):
    global registers, command_registers, timeout_flag
    if regType == 0:
        command_registers [reg] = value
    elif regType == 1:
        timeout_flag = value
    elif regType == 2:
        registers [reg] = value

def execAdd (lRegType, lReg, rRegType, rReg, dRegType, dReg):
    to_write = readReg (lRegType, lReg) + readReg (rRegType, rReg)
    writeReg (dRegType, dReg, to_write)

def execMovr (srcRegType, srcReg, destRegType, destReg):
    writeReg (destRegType, destReg, readReg (srcRegType, srcReg))

def execUNot (srcRegType, srcReg, destRegType, destReg):
    writeReg (destRegType, destReg, int (not readReg (srcRegType, srcReg)))

def execMovc (const, regType, reg):
    writeReg (regType, reg, const)

def execUSubc (const, regType, reg):
    writeReg (regType, reg, -const)

def execInvc (const, regType, reg):
    writeReg (regType, reg, ~const)

def execNotc (const, regType, reg):
    writeReg (regType, reg, not const)

def execTimeoutcr (const):
    global timeout_value, timeout_set, timeout_flag
    timeout_flag = 0
    timeout_set = True
    timeout_value = const

def execFetch (const):
    global timeout_value, timeout_set, timeout_flag
    if timeout_set:
        start = timer ()
        writeReg (2, 1, int (input (f"Requesting telemetry {const}: ")))
        timeout_value -= (timer () - start) # Subtract the elapsed time
        if timeout_value <= 0:
            timeout_flag = 1
            timeout_set = False
    else:
        timeout_set = False
        timeout_flag = 0
        writeReg (2, 1, int (input (f"Requesting telemetry {const}: ")))

def execJmpzr (regType, reg, jDest, nextInstr):
    return jDest * 8 if readReg (regType, reg) == 0 else nextInstr

def execJmpnzr (regType, reg, jDest, nextInstr):
    return jDest * 8 if readReg (regType, reg) != 0 else nextInstr

def execGtc (const, srcRegType, srcReg, destRegType, destReg):
    to_write = readReg (srcRegType, srcReg) > const
    writeReg (destRegType, destReg, to_write)

def execLtc (const, srcRegType, srcReg, destRegType, destReg):
    to_write = readReg (srcRegType, srcReg) < const
    writeReg (destRegType, destReg, to_write)

def execShiftcl (const, srcRegType, srcReg, destRegType, destReg):
    to_write = readReg (srcRegType, srcReg) << const
    writeReg (destRegType, destReg, to_write)

def rshiftHelp (val, n): return (val % 0x100000000) >> n

def execShiftcrl (const, srcRegType, srcReg, destRegType, destReg):
    to_write = rshiftHelp (readReg (srcRegType, srcReg), const)
    writeReg (destRegType, destReg, to_write)

def execOrrb (lRegType, lReg, rRegType, rReg, dRegType, dReg):
    to_write = readReg (lRegType, lReg) | readReg (rRegType, rReg)
    writeReg (dRegType, dReg, to_write)

def execSend (const):
    cmd = c_uint32 (readReg (0, 0))
    cmd = f"{cmd.value:0{32}b}"
    print (f"Sending command {const}: {cmd}")

dispatcher = {
    (0, 0) : execAdd,
    (0, 1) : execAdd, 
    (0, 2) : execAdd,
    (0, 41) : execOrrb,
    (1, 0) : execMovr,
    (1, 4) : execUNot,
    (2, 34) : execGtc,
    (2, 37) : execLtc,
    (2, 42) : execShiftcl,
    (2, 43) : execShiftcrl,
    (3, 0) : execMovc,
    (3, 1) : execUSubc,
    (3, 2) : execUSubc,
    (3, 3) : execInvc,
    (3, 4) : execNotc,
    (4, 2) : execTimeoutcr,
    (4, 4) : execFetch,
    (4, 6) : execSend,
    (6, 0) : execJmpzr,
    (6, 1) : execJmpnzr
}