from subprocess import call
from os.path import join

wesnoth_dir = r"C:\Users\Ravana\Desktop\general\wesnoth-related\dev1.13.8"
wesnoth_path = join(wesnoth_dir,"wesnoth-1.13.8.exe")
core_path = join(wesnoth_dir,"data")

core_out_path = join("..","core")

# it must be in actual userdata
userdata_path = r"C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6\userdata"
input_path = r"C:\Users\Ravana\Desktop\general\wesnoth-related\mydev1.12.6\userdata\data\add-ons\Ageless_Era"
addon_out_path = join("..","preprocessed_addon")

call([wesnoth_path, "--preprocess-defines", "MULTIPLAYER,SKIP_CORE", "-p", core_path, core_out_path, "--preprocess-output-macros"])

call([wesnoth_path, "--userdata-dir", userdata_path, "--preprocess-defines", "MULTIPLAYER,SKIP_CORE", "--preprocess-input-macros", join(core_out_path, "_MACROS_.cfg"), "-p", input_path, addon_out_path])