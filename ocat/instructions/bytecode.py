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

class Opcode (Field):
    def __init__ (self, value):
        super ().__init__ (value, 8)

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
    # Perform an operation on registers in left and right, store in dest register
    def __init__ (self, left, right, dest):
        self.opcode = None
        self.left = left
        self.right = right
        self.dest = dest

    def setFields (self):
        self.fields = [
            Opcode (self.opcode),
            Register (self.left),
            Register (self.right),
            Register (self.dest)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.left}, {self.right}, {self.dest}"

class UnaryR (ByteInstruction):
    # Perform an operation on register in reg, store in dest register
    def __init__ (self, reg, dest):
        self.opcode = None
        self.reg = reg
        self.dest = dest

    def setFields (self):
        self.fields = [
            Opcode (self.opcode),
            Register (self.reg),
            Register (self.dest)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.reg}, {self.dest}"

class BinaryC (ByteInstruction):
    # Perform an operation on register in left and constant right, store in dest register
    def __init__ (self, left, right, dest):
        self.opcode = None
        self.left = left
        self.right = right
        self.dest = dest

    def setFields (self):
        self.fields = [
            Opcode (self.opcode),
            Constant (self.left),
            Register (self.right),
            Register (self.dest)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.left}, {self.right}, {self.dest}"

class UnaryC (ByteInstruction):
    # Perform an operation on constant in reg, store in dest register
    def __init__ (self, reg, dest):
        self.opcode = None
        self.reg = reg
        self.dest = dest

    def setFields (self):
        self.fields = [
            Opcode (self.opcode),
            Constant (self.reg),
            Register (self.dest)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.reg}, {self.dest}"

class Function (ByteInstruction):
    # Perform an operation on constant in reg, store in dest register
    def __init__ (self, id):
        self.opcode = None
        self.id = id

    def setFields (self):
        self.fields = [
            Opcode (self.opcode),
            MessageId (self.id)
        ]

    def __repr__ (self):
        return f"{type(self).__name__.lower()} {self.id}"

########################
# Move instructions
########################

class Movr (UnaryR):
    # Move register src to register dest
    def __init__ (self, src, dest):
        self.opcode = 0
        self.src = src
        self.dest = dest
    
    def setFields (self):
        self.fields = [
            Opcode (self.opcode),
            Register (self.src),
            Register (self.dest)
        ]

    def __repr__ (self):
        return f"movr {self.src}, {self.dest}"

class Movc (UnaryC):
    # Move constant src to register dest
    def __init__ (self, src, dest):
        self.opcode = 1
        self.src = src
        self.dest = dest

    def setFields (self):
        self.fields = [
            Opcode (self.opcode),
            Constant (self.src),
            Register (self.dest)
        ]

    def __repr__ (self):
        return f"movc {self.src}, {self.dest}"

################################################
# BinaryR Arithmetic Instructions
################################################

class Addr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 2
        super ().__init__ (left, right, dest)

class Subr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 3
        super ().__init__ (left, right, dest)

class Mulr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 4
        super ().__init__ (left, right, dest)

class Divr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 5
        super ().__init__ (left, right, dest)

class Expr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 6
        super ().__init__ (left, right, dest)

class Modr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 7
        super ().__init__ (left, right, dest)

class Andlr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 8
        super ().__init__ (left, right, dest)

class Xorlr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 9
        super ().__init__ (left, right, dest)

class Eqr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 10
        super ().__init__ (left, right, dest)

class Neqr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 11
        super ().__init__ (left, right, dest)

class Expr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 12
        super ().__init__ (left, right, dest)

class Gter (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 13
        super ().__init__ (left, right, dest)

class Lter (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 14
        super ().__init__ (left, right, dest)

class Gtr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 15
        super ().__init__ (left, right, dest)

class Ltr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 16
        super ().__init__ (left, right, dest)

class Orlr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 17
        super ().__init__ (left, right, dest)

class Andbr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 18
        super ().__init__ (left, right, dest)

class Xorbr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 19
        super ().__init__ (left, right, dest)

class Orbr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 20
        super ().__init__ (left, right, dest)

class Shiftlr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 21
        super ().__init__ (left, right, dest)

class Shiftrr (BinaryR):
    def __init__ (self, left, right, dest):
        self.opcode = 22
        super ().__init__ (left, right, dest) 

################################################
# UnaryR Arithmetic Instructions
################################################

class USubr (UnaryR):
    def __init__ (self, reg, dest):
        self.opcode = 23
        super ().__init__ (reg, dest) 

class Invr (UnaryR):
    def __init__ (self, reg, dest):
        self.opcode = 24
        super ().__init__ (reg, dest) 

class Notr (UnaryR):
    def __init__ (self, reg, dest):
        self.opcode = 25
        super ().__init__ (reg, dest) 

################################################
# BinaryC Arithmetic Instructions
################################################

class Addc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 26
        super ().__init__ (left, right, dest)

class Subc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 27
        super ().__init__ (left, right, dest)

class Mulc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 28
        super ().__init__ (left, right, dest)

class Divc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 29
        super ().__init__ (left, right, dest)

class Expc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 30
        super ().__init__ (left, right, dest)

class Modc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 31
        super ().__init__ (left, right, dest)

class Andlc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 32
        super ().__init__ (left, right, dest)

class Xorlc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 33
        super ().__init__ (left, right, dest)

class Eqc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 34
        super ().__init__ (left, right, dest)

class Neqc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 35
        super ().__init__ (left, right, dest)

class Expc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 36
        super ().__init__ (left, right, dest)

class Gtec (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 37
        super ().__init__ (left, right, dest)

class Ltec (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 38
        super ().__init__ (left, right, dest)

class Gtc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 39
        super ().__init__ (left, right, dest)

class Ltc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 40
        super ().__init__ (left, right, dest)

class Orlc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 41
        super ().__init__ (left, right, dest)

class Andbc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 42
        super ().__init__ (left, right, dest)

class Xorbc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 43
        super ().__init__ (left, right, dest)

class Orbc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 44
        super ().__init__ (left, right, dest)

class Shiftlc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 45
        super ().__init__ (left, right, dest)

class Shiftrc (BinaryC):
    def __init__ (self, left, right, dest):
        self.opcode = 46
        super ().__init__ (left, right, dest) 

################################################
# UnaryC Arithmetic Instructions
################################################

class USubc (UnaryC):
    def __init__ (self, reg, dest):
        self.opcode = 47
        super ().__init__ (reg, dest) 

class Invc (UnaryC):
    def __init__ (self, reg, dest):
        self.opcode = 48
        super ().__init__ (reg, dest) 

class Notc (UnaryC):
    def __init__ (self, reg, dest):
        self.opcode = 49
        super ().__init__ (reg, dest) 

############################
# Send and Fetch Instructions
############################

class Send (Function):
    def __init__ (self, id):
        self.opcode = 50
        super ().__init__ (id)

class Fetch (Function):
    def __init__ (self, id):
        self.opcode = 51
        super ().__init__ (id)

class FetchN (Function):
    def __init__ (self, id):
        self.opcode = 52
        super ().__init__ (id)