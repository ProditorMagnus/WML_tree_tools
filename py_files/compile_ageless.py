from subprocess import call
from os.path import join

versions = ["1.13", "1.12", "ghype"]
version = "ghype"
assert version in versions

if version == "1.13":
    wesnoth_dir = r"C:\Users\Ravana\Desktop\general\wesnoth-related\dev1.13.11"
    wesnoth_path = join(wesnoth_dir, "wesnoth1_13_11.exe")
    userdata_path = r"C:\Users\Ravana\Documents\My Games\Wesnoth1.13"
    input_path = r"C:\Users\Ravana\Documents\My Games\Wesnoth1.13\data\add-ons\Ageless_Era"
    addon_out_path = join("..", "preprocessed_addon_13")
    core_out_path = join("..", "core_13")
elif version == "ghype":
    wesnoth_dir = r"C:\Users\Ravana\Desktop\general\wesnoth-related\stable1.12.5copy"
    wesnoth_path = join(wesnoth_dir, "wesnoth-1.12.5stablecopy.exe")
    userdata_path = r"C:\Users\Ravana\Desktop\general\wesnoth-related\stable1.12.5copy\userdata"
    input_path = r"C:\Users\Ravana\Desktop\general\wesnoth-related\stable1.12.5copy\userdata\data\add-ons\Ageless_Era"
    addon_out_path = join("..", "preprocessed_addon_ghype")
    core_out_path = join("..", "core_ghype")
else:
    wesnoth_dir = r"C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6"
    wesnoth_path = join(wesnoth_dir, "wesnoth-mydev.exe")
    userdata_path = r"C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6\userdata"
    input_path = r"C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6\userdata\data\add-ons\Ageless_Era"
    addon_out_path = join("..", "preprocessed_addon")
    core_out_path = join("..", "core")
core_path = join(wesnoth_dir, "data")

call([wesnoth_path, "--data-dir", wesnoth_dir, "--preprocess-defines", "MULTIPLAYER,SKIP_CORE", "-p", core_path,
      core_out_path, "--preprocess-output-macros"])

call([wesnoth_path, "--data-dir", wesnoth_dir, "--userdata-dir", userdata_path, "--preprocess-defines",
      "MULTIPLAYER,SKIP_CORE", "--preprocess-input-macros", join(core_out_path, "_MACROS_.cfg"), "-p", input_path,
      addon_out_path])
