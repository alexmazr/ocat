# Byte code instructions for OCat
# Instructions are formatted into types based on their parameters so r1 has one register, c1 has one constant, cr2 has a constant and a register
# Instructions are meant to read left to right, i.e. movr r1, r2 -> move register r1 to r2
#  or addi 45, r1, r3 -> add int 45 to r1 and store in r3


# Instruction types:
#  Binary R-Type
#  Unary R-Type
#  Binary C-Type
#  Unary C-Type
#  Function F-Type

byte_endian = 'big'
bit_endian = 'big'

class Field:
    def __init__ (self, value, size):
        self.value = value
        self.size = size

class InstrType (Field):
    size = 3
    def __init__ (self, value):
        super ().__init__ (value, self.size)

class WaitType (Field):
    size = 1
    def __init__ (self, value):
        super ().__init__ (value, self.size)

class Opcode (Field):
    size = 6
    def __init__ (self, value):
        super ().__init__ (value, self.size)

class Register (Field):
    size = 6
    def __init__ (self, value):
        to_write = 0
        if value[0] == 't':
            to_write = 16
        elif value[0] == 'r':
            to_write = 32
        to_write = to_write | int (value[1:])
        super ().__init__ (to_write, self.size)

class Constant (Field):
    size = 32
    def __init__ (self, value):
        super ().__init__ (value, self.size)

class MessageId (Field):
    size = 8
    def __init__ (self, value):
        super ().__init__ (value, self.size)

class Padding (Field):
    def __init__ (self, size):
        super ().__init__ (0, size)

class ProgramCounter (Field):
    size = 16
    def __init__ (self, value):
        super ().__init__ (value, self.size)

class ByteInstruction:
    def __init__ (self):
        self.fields = []

    def pack (self):
        global byte_endian, bit_endian
        bitstring = ''
        fields = self.fields
        if byte_endian == 'little':
            fields = fields[::-1]
        for field in fields:
            bitfield = f"{field.value:0{field.size}b}"
            if bit_endian == 'little':
                bitfield = bitfield[::-1] # reverse a bit
            bitstring += bitfield
        return bitstring.encode ()

class BinaryR (ByteInstruction):
    sizeInBits = InstrType.size + Opcode.size + (Register.size * 3) + Padding (5).size
    sizeInBytes = int (sizeInBits / 8)

    def __init__ (self, left, right, dest):
        self.opcode = None
        self.left = left
        self.right = right
        self.dest = dest
        self.type = 0

    def setFields (self):
        self.fields = [
            InstrType (self.type),
            Opcode (self.opcode),
            Register (self.left),
            Register (self.right),
            Register (self.dest),
            Padding (5)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.left}, {self.right}, {self.dest}"

class UnaryR (ByteInstruction):
    sizeInBits = InstrType.size + Opcode.size + (Register.size * 2) + Padding (3).size
    sizeInBytes = int (sizeInBits / 8)

    def __init__ (self, reg, dest):
        self.opcode = None
        self.reg = reg
        self.dest = dest
        self.type = 1

    def setFields (self):
        self.fields = [
            InstrType (self.type),
            Opcode (self.opcode),
            Register (self.reg),
            Register (self.dest),
            Padding (3)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.reg}, {self.dest}"

class BinaryC (ByteInstruction):
    sizeInBits = InstrType.size + Opcode.size + Constant.size + (Register.size * 2) + Padding (3).size
    sizeInBytes = int (sizeInBits / 8)
    def __init__ (self, left, right, dest):
        self.opcode = None
        self.left = left
        self.right = right
        self.dest = dest
        self.type = 2

    def setFields (self):
        self.fields = [
            InstrType (self.type),
            Opcode (self.opcode),
            Constant (self.left),
            Register (self.right),
            Register (self.dest),
            Padding (3)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.left}, {self.right}, {self.dest}"

class UnaryC (ByteInstruction):
    sizeInBits = InstrType.size + Opcode.size + Constant.size + Register.size + Padding (1).size
    sizeInBytes = int (sizeInBits / 8)

    def __init__ (self, reg, dest):
        self.opcode = None
        self.reg = reg
        self.dest = dest
        self.type = 3

    def setFields (self):
        self.fields = [
            InstrType (self.type),
            Opcode (self.opcode),
            Constant (self.reg),
            Register (self.dest),
            Padding (1)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.reg}, {self.dest}"

class SingleC (ByteInstruction):
    sizeInBits = InstrType.size + Opcode.size + Constant.size + Padding (7).size
    sizeInBytes = int (sizeInBits / 8)

    def __init__ (self, const):
        self.opcode = None
        self.const = const
        self.type = 4
        
    def setFields (self):
        self.fields = [
            InstrType (self.type),
            Opcode (self.opcode),
            Constant (self.const),
            Padding (7)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.const}"

class SingleR (ByteInstruction):
    sizeInBits = InstrType.size + Opcode.size + Register.size + Padding (1).size
    sizeInBytes = int (sizeInBits / 8)

    def __init__ (self, reg):
        self.opcode = None
        self.reg = reg
        self.type = 5
        

    def setFields (self):
        self.fields = [
            InstrType (self.type),
            Opcode (self.opcode),
            Register (self.reg),
            Padding (1)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.reg}"

class JumpR (ByteInstruction):
    sizeInBits = InstrType.size + Opcode.size + Register.size + ProgramCounter.size + Padding (1).size
    sizeInBytes = int (sizeInBits / 8)

    def __init__ (self, reg, pc):
        self.opcode = None
        self.pc = pc
        self.reg = reg
        self.type = 6
        

    def setFields (self):
        self.fields = [
            InstrType (self.type),
            Opcode (self.opcode),
            Register (self.reg),
            ProgramCounter (self.pc),
            Padding (1)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.reg}, {self.pc}"