from .compiler import compile
import sys



if __name__ == "__main__":
    config_root_path = "config/"
    config_type = "json"

    cmd_config_name = "commands."
    tlm_config_name = "telemetry."

    args = len (sys.argv)
    if args > 3:
        config_type = sys.argv [3]
    if args > 2:
        config_root_path = sys.argv [2]
    if args > 1:
        cmd_path = f"{config_root_path}{cmd_config_name}{config_type}"
        tlm_path = f"{config_root_path}{tlm_config_name}{config_type}"
        compile (sys.argv[1], cmd_path, tlm_path)
    if args <= 1:
        print ("Please specify a path to compile")