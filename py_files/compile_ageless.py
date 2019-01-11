#!/usr/bin/python3
import os
from subprocess import call
from os.path import join, expanduser

versions = ["1.14"]
version = "1.14"
assert version in versions


def printNewLogFiles(log_path, log_files):
    log_files = set(os.listdir(log_path)).difference(log_files)
    for file in log_files:
        with open(join(log_path, file)) as f:
            print()
            print(f.read())


def preprocess_addon(addonId, preprocess_defines="MULTIPLAYER,SKIP_CORE", OS="windows"):
    def isWindows():
        return OS == "windows"

    log_files = set()
    log_path = None
    if isWindows():
        wesnoth_dir = r"C:\Program Files (x86)\Steam\steamapps\common\wesnoth"
        wesnoth_exe = r"C:\Program Files (x86)\Steam\steamapps\common\wesnoth\wesnoth.exe"
        userdata_path = r"C:\Users\Ravana\Documents\My Games\Wesnoth1.14"
        input_path = r"C:\Users\Ravana\Documents\My Games\Wesnoth1.14\data\add-ons\{}".format(addonId)
        log_path = expanduser(join(userdata_path, "logs"))
        log_files = set(os.listdir(log_path))
    else:
        wesnoth_dir = r"~/wesnoth/wesnoth-lobby"
        wesnoth_exe = r"~/wesnoth/wesnoth-lobby/wesnoth"
        userdata_path = r"~/wesnoth/userdata_1_14"
        input_path = r"~/wesnoth/userdata_1_14/data/add-ons/{}".format(addonId)
    addon_out_path = join("..", "preprocessed_addon", addonId)
    core_out_path = join("..", "core")
    core_path = expanduser(join(wesnoth_dir, "data"))
    wesnoth_dir = expanduser(wesnoth_dir)
    wesnoth_exe = expanduser(wesnoth_exe)
    userdata_path = expanduser(userdata_path)
    input_path = expanduser(input_path)
    addon_out_path = expanduser(addon_out_path)
    core_out_path = expanduser(core_out_path)

    call([wesnoth_exe, "--data-dir", wesnoth_dir, "--preprocess-defines", preprocess_defines, "-p", core_path,
          core_out_path, "--preprocess-output-macros"])
    if isWindows():
        printNewLogFiles(log_path, log_files)

    call([wesnoth_exe, "--data-dir", wesnoth_dir, "--userdata-dir", userdata_path, "--preprocess-defines",
          preprocess_defines, "--preprocess-input-macros", join(core_out_path, "_MACROS_.cfg"), "-p", input_path,
          addon_out_path])
    if isWindows():
        printNewLogFiles(log_path, log_files)


if __name__ == '__main__':
    preprocess_addon("Ageless_Era")
