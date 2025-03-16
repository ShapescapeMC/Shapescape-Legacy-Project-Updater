from pathlib import Path
import re
import json

SETBLOCK = re.compile(
	r'(setblock)\s+'
	r'((?:(?:[~^]-?[\d\.]*\s*)|(?:[-^]?[\d\.]*\s*)){3})\s+'
	r'([a-zA-Z0-9_:"]*[a-zA-Z][a-zA-Z0-9_:"]*)\s+'
	r'([-?\d+]+)')

# fill ~~~ ~~~ stone 1 replace dirt 1
FILL_REPLACE_0 = re.compile(
	r'(fill)\s+'
	r'((?:(?:[~^]-?[\d\.]*\s*)|(?:[-^]?[\d\.]*\s*)){3})\s+'
	r'((?:(?:[~^]-?[\d\.]*\s*)|(?:[-^]?[\d\.]*\s*)){3})\s+'
	r'([a-zA-Z0-9_:"]*[a-zA-Z][a-zA-Z0-9_:"]*)\s+'
	r'([-?\d+]+)\s+'
	r'(replace)\s+'
	r'([a-zA-Z0-9_:"]*[a-zA-Z][a-zA-Z0-9_:"]*)\s+'
	r'([-?\d+]+)')

# fill ~~~ ~~~ stone replace dirt 1
FILL_REPLACE_1 = re.compile(
	r'(fill)\s+'
	r'((?:(?:[~^]-?[\d\.]*\s*)|(?:[-^]?[\d\.]*\s*)){3})\s+'
	r'((?:(?:[~^]-?[\d\.]*\s*)|(?:[-^]?[\d\.]*\s*)){3})\s+'
	r'([a-zA-Z0-9_:"]*[a-zA-Z][a-zA-Z0-9_:"]*)\s+'
	r'(replace)\s+'
	r'([a-zA-Z0-9_:"]*[a-zA-Z][a-zA-Z0-9_:"]*)\s+'
	r'([-?\d+]+)')

FILL = re.compile(
	r'(fill)\s+'
	r'((?:(?:[~^]-?[\d\.]*\s*)|(?:[-^]?[\d\.]*\s*)){3})\s+'
	r'((?:(?:[~^]-?[\d\.]*\s*)|(?:[-^]?[\d\.]*\s*)){3})\s+'
	r'([a-zA-Z0-9_:"]*[a-zA-Z][a-zA-Z0-9_:"]*)\s+'
	r'([-?\d+]+)')

# if block
EXECUTE = re.compile(
	r'(execute)((?!.*run.*execute).*)(if blocks|if block)+\s+'
	r'((?:(?:[~^]-?[\d\.]*\s*)|(?:[-^]?[\d\.]*\s*)){3})\s+'
	r'([a-zA-Z0-9_:"]*[a-zA-Z][a-zA-Z0-9_:"]*)\s+'
	r'([-?\d+]+)')

def convert_aux(block_id, aux_value, escape=True):
	aux_value = int(aux_value)

	# add namespace
	if not ":" in block_id:
		block_id = "minecraft:"+block_id

	# check if aux is -1 or lower
	if aux_value < 0 or block_id == "minecraft:air":
		return("[]")

	# check if block is on the list
	try:
		result = block_map["blocks"][block_id][aux_value]
		if escape:
			result = result.replace('"', '\\"')
		return(result)

	except Exception as e:
		print("[ERROR] " + "BLOCK: " + str(block_id) + ", AUX: " + str(aux_value) + " | Error: "+ str(e))
		print("	-> Using \"[]\" for the block state instead.")
		return("[]")


def update_blocks(command: str, escape=True) -> tuple[str, bool]:
	'''
	Updates the blocks commands by replacing the aux values with the block states.
	Returns a tuple with the updated command and a boolean that indicates if
	the command was updated.
	'''
	updated = False

	# (setblock) (~ ~ ~) (stone) (1)
	match = re.search(SETBLOCK, command)
	if match:
		#print("SETBLOCK", match.group(3), match.group(4))
		block_state = convert_aux(match.group(3), match.group(4), escape)

		subed, nsub = SETBLOCK.subn(rf'\1 \2 \3 {block_state}', command)
		if nsub > 0:
			command = subed
			updated = True

	# (fill) (~ ~ ~) (~ ~ ~) (stone) (1) (replace) (dirt) (1)
	match = re.search(FILL_REPLACE_0, command)
	if match:
		#print("FILL_REPLACE_0", match.group(4), match.group(5), "|", match.group(7), match.group(8))
		block_state_1 = convert_aux(match.group(4), match.group(5), escape)
		block_state_2 = convert_aux(match.group(7), match.group(8), escape)

		subed, nsub = FILL_REPLACE_0.subn(rf'\1 \2 \3 \4 {block_state_1} \6 \7 {block_state_2}', command)
		if nsub > 0:
			command = subed
			updated = True

	# (fill) (~ ~ ~) (~ ~ ~) (stone) (replace) (dirt) (1)
	match = re.search(FILL_REPLACE_1, command)
	if match:
		#print("FILL_REPLACE_1", match.group(4), "|", match.group(6), match.group(7))
		block_state = convert_aux(match.group(6), match.group(7), escape)

		subed, nsub = FILL_REPLACE_1.subn(rf'\1 \2 \3 \4 \5 \6 {block_state}', command)
		if nsub > 0:
			command = subed
			updated = True

	# (fill) (~ ~ ~) (~ ~ ~) (stone) (1)
	match = re.search(FILL, command)
	if match:
		#print("FILL", match.group(4), match.group(5))
		block_state = convert_aux(match.group(4), match.group(5), escape)

		subed, nsub = FILL.subn(rf'\1 \2 \3 \4 {block_state}', command)
		if nsub > 0:
			command = subed
			updated = True

	# (execute) (...) (if block) (~ ~ ~) (stone) (1)
	match = re.search(EXECUTE, command)
	if match:
		#print("EXECUTE", match.group(5), match.group(6))
		block_state = convert_aux(match.group(5), match.group(6), escape)

		subed, nsub = EXECUTE.subn(rf'\1\2\3 \4 \5 {block_state}', command)
		if nsub > 0:
			command = subed
			updated = True

	return command, updated


def update_file(file_path: Path, escape=True) -> None:
	'''
	Updates the file by replacing the old blocks aux values with the block states.
	This function doesn't care about the syntax of the file. It is treated as
	a plain text file.
	'''
	needs_updating: bool = False
	with open(file_path, 'r', encoding='utf-8') as f:
		lines: list[str] = f.readlines()

	for i in range(len(lines)):
		# Loop with replacements until there is nothing to replace
		updated_blocks, is_updated = update_blocks(lines[i], escape)
		if is_updated:
			lines[i] = updated_blocks
			needs_updating = True

	if needs_updating:
		with open(file_path, 'w', encoding='utf-8') as f:
			print(f'Updating blocks in {file_path.as_posix()}')
			f.writelines(lines)


def main_old() -> None:
	config: dict[str, Path] = {
		"bp_path": Path("BP")
	}

	path_functions: Path = Path(config["bp_path"] / 'functions')
	for function in path_functions.rglob("*.mcfunction"):
		update_file(function, escape=False)

	path_bp_anims: Path = Path(config["bp_path"] / 'animations')
	for bp_anim in path_bp_anims.rglob("*.json"):
		update_file(bp_anim)

	path_bp_acs: Path = Path(config["bp_path"] / 'animation_controllers')
	for bp_ac in path_bp_acs.rglob("*.json"):
		update_file(bp_ac)

	path_dialogues: Path = Path(config["bp_path"] / 'dialogue')
	for dialogue in path_dialogues.rglob("*.json"):
		update_file(dialogue)

def main():
	# Read aux values and block states
	global block_map
	with open("data/shapescape_legacy_project_updater/block_map.json", "r") as f:
		block_map = json.load(f)

	# print("\n", "[!] If you have old execute, remember to run me AFTER execute_updater. This works for 1.20.10+", "\n")
	main_old()

if __name__ == "__main__":
	main()
