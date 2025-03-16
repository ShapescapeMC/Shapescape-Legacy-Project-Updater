from pathlib import Path
import re

SUMMON = re.compile(
	r'(summon)\s+'
	r'([A-Za-z0-9_:]+)\s+'
	r'((?:(?:[~^]-?[\d\.]*\s*)|(?:[-^]?[\d\.]*\s*)){3})\s+'
	r'((?=.*[a-zA-Z])[a-zA-Z0-9_:"]+)')

def update_summon(command: str) -> tuple[str, bool]:
	'''
	Updates the summon commands by replacing the old syntax with the new one.
	Returns a tuple with the updated command and a boolean that indicates if
	the command was updated.
	'''
	updated = False
	subed, nsub = SUMMON.subn(r'\1 \2 \3 ~ ~ \4', command)
	if nsub > 0:
		command = subed
		updated = True
	return command, updated


def update_file(file_path: Path) -> None:
	'''
	Updates the file by replacing the old summon syntax with the new one.
	This function doesn't care about the syntax of the file. It is treated as
	a plain text file.
	'''
	needs_updating: bool = False
	with open(file_path, 'r', encoding='utf-8') as f:
		lines: list[str] = f.readlines()

	for i in range(len(lines)):
		# Loop with replacements until there is nothing to replace
		updated_summon, is_updated = update_summon(lines[i])
		if is_updated:
			lines[i] = updated_summon
			needs_updating = True

	if needs_updating:
		with open(file_path, 'w', encoding='utf-8') as f:
			print(f'Updating summon in {file_path.as_posix()}')
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