class VarData:
    def __init__ (self, type, mutable):
        self.type = type
        self.mutable = mutable

    def __repr__ (self):
        if self.mutable:
            return f"is a mutable {self.type}"
        return f"is an immutable {self.type}"

env = {}

# This is a "fake" object that essentially wraps the above env global
#  This is just an attempt to make the api clean is less prone to errors
#  It does assume the user ONLY imports the Environment class
class Environment:
    def __init__ (self):
        pass

    def push (self, name, type, mutable):
        global env
        env [name] = VarData (type, mutable)

    def getType (self, name):
        global env
        return env [name].type
    
    def updateType (self, name, type):
        global env
        env [name].type = type
    
    def peek (self, name):
        global env
        return env [name]

    def __contains__ (self, name):
        global env
        return name in env 

    def dump (self):
        global env
        for name, data in env.items ():
            print (f"\t{name} {data}")