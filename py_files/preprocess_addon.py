from subprocess import call
from os.path import join

wesnoth_dir = r"C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6"
wesnoth_path = join(wesnoth_dir,"wesnoth-mydev.exe")
core_path = join(wesnoth_dir,"data")

core_out_path = join("..","core")

# it must be in actual userdata
userdata_path = r"C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6\userdata"
input_path = r"C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6\userdata\data\add-ons\Ageless_Era"
addon_out_path = join("..","preprocessed_addon")

# Something breaks when calling it from script
working_core = r"""C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6>wesnoth-mydev.exe --
preprocess-defines MULTIPLAYER,SKIP_CORE -p "C:\Users\Ravana\Desktop\general\wes
noth-related\mydev1.12.6\data" "C:\Users\Ravana\Desktop\general\wesnoth-related\
dev1.13.8\WML_tree_tools\core" --preprocess-output-macros
"""
# print(" ".join([wesnoth_path, "--preprocess-defines", "MULTIPLAYER,SKIP_CORE", "-p", core_path, core_out_path, "--preprocess-output-macros"]))
call([wesnoth_path, "--data-dir", wesnoth_dir, "--preprocess-defines", "MULTIPLAYER,SKIP_CORE", "-p", core_path, core_out_path, "--preprocess-output-macros"])

working_addon = r"""C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6>wesnoth-mydev.exe --
userdata-dir "C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6\userda
ta" --preprocess-defines MULTIPLAYER,SKIP_CORE --preprocess-input-macros "C:\Use
rs\Ravana\Desktop\general\wesnoth-related\dev1.13.8\WML_tree_tools\core\_MACROS_
.cfg" -p "C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6\userdata\d
ata\add-ons\Ageless_Era" "C:\Users\Ravana\Desktop\general\wesnoth-related\dev1.1
3.8\WML_tree_tools\preprocessed_addon"
"""
# print(" ".join([wesnoth_path, "--userdata-dir", userdata_path, "--preprocess-defines", "MULTIPLAYER,SKIP_CORE", "--preprocess-input-macros", join(core_out_path, "_MACROS_.cfg"), "-p", input_path, addon_out_path]))
call([wesnoth_path, "--data-dir", wesnoth_dir, "--userdata-dir", userdata_path, "--preprocess-defines", "MULTIPLAYER,SKIP_CORE", "--preprocess-input-macros", join(core_out_path, "_MACROS_.cfg"), "-p", input_path, addon_out_path])