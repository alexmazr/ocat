import eel
from cmd.compiler import compile

eel.init('gui')

@eel.expose
def handleCompile (text):
    try:
        return str (compile (text))
    except Exception as e:
        return str (e)

@eel.expose
def color ():
    pass

eel.start('index.html', port=0, cmdline_args=['--chrome-frame  --kiosk'])