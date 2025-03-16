from pathlib import Path
import re

# NOTE: The regex part that captures the coordinates allows empty strings,
# which isn't exactly correct, but it shouldn't cause any issues to the user.
# NOTE: The regex pattern always treats the selectors that use the @initiator
# as valid execute even though it's only allowed in dialogues.
EXECUTE = re.compile(
    r'(execute)\s+((?:@.\[+[^\[\]]+?\]+)|(?:@.)|@initiator)\s+'
    r'((?:(?:[~^]-?[\d\.]*\s*)|(?:[-^]?[\d\.]*\s*)){3})')
EXECUTE_DETECT = re.compile(
    r'(execute)\s+((?:@.\[+[^\[\]]+?\]+)|(?:@.{1})|@initiator)\s+'
    r'((?:(?:[~^]-?[\d\.]*\s*)|(?:-?[\d\.]*\s*)){3})\s+(detect)\s+'
    r'((?:(?:[~^]-?[\d\.]*\s*)|(?:-?[\d\.]*\s*)){3})\s+(\S*\s)(-?\d+)')

def print_yellow(text: str) -> None:
    text_list = text.split('\n')
    for line in text_list:
        print(f'\033[33m{line}\033[0m')

def update_execute(command: str) -> tuple[str, bool, bool]:
    '''
    Updates the execute commands by replacing the old syntax with the new one.
    Returns a tuple with the updated command and a boolean that indicates if
    the command was updated.
    '''
    updated = False

    # Execcute command changed from numerical block variants to properties.
    # This filter is not able to handle that and only the "-1" value is mapped
    # correctly (-1 means "any variant"). In case of other, specific variants
    # a warning should be shown to the user.
    has_unmappable_blocks = False
    for match in EXECUTE_DETECT.finditer(command):
        if match[6] != '-1':
            has_unmappable_blocks = True
            break
    # Try replacing the execute detect syntax first
    subed, nsub = EXECUTE_DETECT.subn(
        r'\1 as \2 at @s positioned \3 if block \5 \6 run', command)
    if nsub > 0:
        command = subed
        updated = True
    # At this point, all execute detect commands have been replaced with the
    # new syntax, so we can replace the rest of the execute commands.
    subed, nsub = EXECUTE.subn(r'\1 as \2 at @s positioned \3run ', command)
    if nsub > 0:
        command = subed
        updated = True
    return command, updated, has_unmappable_blocks

def update_file(file_path: Path) -> None:
    '''
    Updates the file by replacing the old execute syntax with the new one.
    This functino doesn't care about the syntax of the file. It is treated as
    a plain text file.
    '''
    needs_updating: bool = False
    with open(file_path, 'r', encoding='utf-8') as f:
        lines: list[str] = f.readlines()

    for i in range(len(lines)):
        # Loop with replacements until there is nothing to replace
        updated_execute, is_updated, has_unmappable_blocks = update_execute(
            lines[i])
        if has_unmappable_blocks:
            print_yellow(
                "The execute command detects a block with a "
                "numeric variant. Only the value -1 can be "
                "converted correctly. "
                f"FILE: {file_path} AT LINE: {i + 1}"
        )
        if is_updated:
            lines[i] = updated_execute
            needs_updating = True

    if needs_updating:
        with open(file_path, 'w', encoding='utf-8') as f:
            print(f'Updating execute in {file_path.as_posix()}')
            f.writelines(lines)


def main() -> None:
    config: dict[str, Path] = {
        "bp_path": Path("BP")
    }

    path_functions: Path = Path(config["bp_path"] / 'functions')
    for function in path_functions.rglob("*.mcfunction"):
        update_file(function)

    path_bp_anims: Path = Path(config["bp_path"] / 'animations')
    for bp_anim in path_bp_anims.rglob("*.json"):
        update_file(bp_anim)

    path_bp_acs: Path = Path(config["bp_path"] / 'animation_controllers')
    for bp_ac in path_bp_acs.rglob("*.json"):
        update_file(bp_ac)

    path_dialogues: Path = Path(config["bp_path"] / 'dialogue')
    for dialogue in path_dialogues.rglob("*.json"):
        update_file(dialogue)

if __name__ == "__main__":
    main()