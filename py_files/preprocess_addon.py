from subprocess import call
from os.path import join
import os

wesnoth_dir = r"C:\Users\Ravana\Desktop\general\wesnoth-related\dev1.13.8"
wesnoth_path = join(wesnoth_dir,"wesnoth.exe")
core_path = join(wesnoth_dir,"data")

core_out_path = join("..","core")
input_path = join("..","unprocessed_addon")
addon_out_path = join("..","preprocessed_addon")

for addon_folder in os.listdir(input_path):
	input_path = join(input_path, addon_folder)
	print("Found addon",input_path)
	break

call([wesnoth_path, "--preprocess-defines", "MULTIPLAYER", "-p", core_path, core_out_path, "--preprocess-output-macros"])

call([wesnoth_path, "--preprocess-defines", "MULTIPLAYER", "--preprocess-input-macros", join(core_out_path, "_MACROS_.cfg"), "-p", input_path, addon_out_path])