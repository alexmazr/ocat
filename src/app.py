import eel
from parser import parse

eel.init('gui')

@eel.expose
def compile (text):
    try:
        return str (parse (text))
    except Exception as e:
        return str (e)

@eel.expose
def color ():
    pass

eel.start('index.html', port=0)