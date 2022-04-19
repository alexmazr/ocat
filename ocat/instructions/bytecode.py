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
    def __init__ (self, value):
        super ().__init__ (value, 3)

class WaitType (Field):
    def __init__ (self, value):
        super ().__init__ (value, 1)

class Opcode (Field):
    def __init__ (self, value):
        super ().__init__ (value, 6)

class Register (Field):
    def __init__ (self, value):
        super ().__init__ (int (value [1:]), 4)

class Constant (Field):
    def __init__ (self, value):
        super ().__init__ (value, 32)

class MessageId (Field):
    def __init__ (self, value):
        super ().__init__ (value, 8)

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
        return bitstring

class BinaryR (ByteInstruction):
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
            Register (self.dest)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.left}, {self.right}, {self.dest}"

class UnaryR (ByteInstruction):
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
            Register (self.dest)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.reg}, {self.dest}"

class BinaryC (ByteInstruction):
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
            Register (self.dest)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.left}, {self.right}, {self.dest}"

class UnaryC (ByteInstruction):
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
            Register (self.dest)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.reg}, {self.dest}"

class Function (ByteInstruction):
    def __init__ (self):
        self.opcode = None
        self.type = 4

    def setFields (self):
        self.fields = [
            InstrType (self.type),
            Opcode (self.opcode)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()}"

class SingleC (ByteInstruction):
    def __init__ (self, const):
        self.opcode = None
        self.const = const
        self.type = 5

    def setFields (self):
        self.fields = [
            InstrType (self.type),
            Opcode (self.opcode),
            Constant (self.const)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.const}"

class SingleR (ByteInstruction):
    def __init__ (self, reg):
        self.opcode = None
        self.reg = reg
        self.type = 6

    def setFields (self):
        self.fields = [
            InstrType (self.type),
            Opcode (self.opcode),
            Register (self.reg)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.reg}"