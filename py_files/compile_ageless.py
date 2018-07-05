#!/usr/bin/python3
from subprocess import call
from os.path import join, expanduser

versions = ["1.14"]
version = "1.14"
assert version in versions

# if version == "1.14":
wesnoth_dir = r"~/wesnoth/wesnoth-lobby"
wesnoth_exe = r"~/wesnoth/wesnoth-lobby/wesnoth"
userdata_path = r"~/wesnoth/userdata_1_14"
input_path = r"~/wesnoth/userdata_1_14/data/add-ons/Ageless_Era"
addon_out_path = join("..", "preprocessed_addon")
core_out_path = join("..", "core")

core_path = expanduser(join(wesnoth_dir, "data"))

wesnoth_dir = expanduser(wesnoth_dir)
wesnoth_exe = expanduser(wesnoth_exe)
userdata_path = expanduser(userdata_path)
input_path = expanduser(input_path)
addon_out_path = expanduser(addon_out_path)
core_out_path = expanduser(core_out_path)

preprocess_defines = "MULTIPLAYER,SKIP_CORE"
call([wesnoth_exe, "--data-dir", wesnoth_dir, "--preprocess-defines", preprocess_defines, "-p", core_path,
      core_out_path, "--preprocess-output-macros"])

call([wesnoth_exe, "--data-dir", wesnoth_dir, "--userdata-dir", userdata_path, "--preprocess-defines",
      preprocess_defines, "--preprocess-input-macros", join(core_out_path, "_MACROS_.cfg"), "-p", input_path,
      addon_out_path])

