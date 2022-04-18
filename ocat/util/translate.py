from ..instructions.ast import *
from ..instructions.bytecode import *

def translate (instructions):
    ocat_ir = []
    for node in instructions:
        match node:
            case (Declare () | Assign ()):
                if isinstance (node.expr, Const):
                    ocat_ir.append (Movc (node.expr.value, node.name))
                elif isinstance (node.expr, Ref):
                    ocat_ir.append (Movr (node.expr.name, node.name))
                elif isinstance (node.expr, Call):
                    # TODO: Resolve command/tlm name to id, maybe do that earlier?
                    id = node.expr.args[0].name
                    if node.expr.name == 'send':
                        # TODO: Need to add instructions for building command
                        ocat_ir.append (Send (id))
                        ocat_ir.append (Movr ('resp', node.name))
                    elif node.expr.name == 'fetch':
                        ocat_ir.append (Fetch (id))
                        ocat_ir.append (Movr ('resp', node.name))
                    elif node.expr.name == 'fetch_new':
                        ocat_ir.append (FetchN (id))
                        ocat_ir.append (Movr ('resp', node.name))
                    else:
                        raise SystemExit (f"Unknown function '{node.expr.name}': {node.linedata.lineno}, {node.linedata.linepos}")
                elif isinstance (node.expr, Add):
                    if isinstance (node.expr.left, Ref):
                        if isinstance (node.expr.right, Ref):
                            ocat_ir.append (Addr (node.expr.left.name, node.expr.right.name, node.name))
                        else:
                            ocat_ir.append (Addc (node.expr.right.value, node.expr.left.name, node.name))
                    else:
                        ocat_ir.append (Addc (node.expr.left.value, node.expr.right.name, node.name))
            case Call ():
                id = node.args[0].name
                if node.name == 'send':
                    # TODO: Need to add instructions for building command
                    ocat_ir.append (Send (id))
                elif node.name == 'fetch':
                    ocat_ir.append (Fetch (id))
                elif node.name == 'fetch_new':
                    ocat_ir.append (FetchN (id))
                else:
                    raise SystemExit (f"Unknown function '{node.name}': {node.linedata.lineno}, {node.linedata.linepos}")
            case _:
                ocat_ir.append (node)
    return ocat_ir