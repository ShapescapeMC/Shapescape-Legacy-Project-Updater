import sys
import json

import block_updater as block_updater
import execute_updater as execute_updater
import summon_updater as summon_updater

def main() -> None:
    settings = {
        "update_execute_commands": True,
        "update_block_commands": True,
        "update_summon_commands": True,
    }
    try:
        settings = settings | json.loads(sys.argv[1])
    except:
        pass

    if settings["update_execute_commands"]:
        print("Updating execute commands...")
        execute_updater.main()
    if settings["update_block_commands"]:
        print("Updating block commands...")
        block_updater.main()
    if settings["update_summon_commands"]:
        print("Updating summon commands...")
        summon_updater.main()

if __name__ == "__main__":
    main()