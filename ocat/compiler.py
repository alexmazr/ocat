from .parser import parser

def compile (filepath):
    with open (filepath) as f:
        print (parser.parse (f.read () + "\n"))
    