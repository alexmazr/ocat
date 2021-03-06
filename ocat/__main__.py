from .compiler import compile
from .runtime import Runtime
import sys



if __name__ == "__main__":
    mission_path = 'config/mission.json'
    cmd_path = 'config/commands.json'
    tlm_path = 'config/telemetry.json'
    if sys.argv [1] == 'run':
        runtime = Runtime (sys.argv [2])
        while True:
            runtime.decode ()
        runtime.dumpReg ()
    else:
        if len (sys.argv) == 2:
            compile (sys.argv[-1], mission_path, cmd_path, tlm_path)
        else:
            compile (sys.argv[-2], mission_path, cmd_path, tlm_path, sys.argv[-1])
