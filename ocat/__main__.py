from .compiler import compile
import sys



if __name__ == "__main__":
    mission_path = 'config/mission.json'
    cmd_path = 'config/commands.json'
    tlm_path = 'config/telemetry.json'
    compile (sys.argv[-1], mission_path, cmd_path, tlm_path)
