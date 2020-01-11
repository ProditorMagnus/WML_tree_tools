#!/usr/bin/python3
import os
import subprocess
from os.path import join, expanduser
import wesnoth_paths


def call(args):
    print("Running", args)
    subprocess.call(args)


def printNewLogFiles(log_path, old_log_files):
    new_log_files = os.listdir(log_path)
    log_files = set(new_log_files).difference(old_log_files)
    for file in log_files:
        with open(join(log_path, file)) as f:
            print()
            print(f.read())
    return old_log_files.union(new_log_files)


def preprocess_addon(addonId, preprocess_defines="MULTIPLAYER,SKIP_CORE,__WML_TREE_TOOLS__"):
    log_files = set()
    log_path = None
    wesnoth_dir = wesnoth_paths.getWesnothDir()
    wesnoth_exe = wesnoth_paths.getWesnothExe()
    userdata_path = wesnoth_paths.getUserdataDir()
    if wesnoth_paths.isWindows():
        input_path = userdata_path + r"\data\add-ons\{}".format(addonId)
        log_path = expanduser(join(userdata_path, "logs"))
        log_files = set(os.listdir(log_path))
    else:
        input_path = userdata_path + "/data/add-ons/{}".format(addonId)
    addon_out_path = join("..", "preprocessed_addon" + str(wesnoth_paths.version), addonId)
    core_out_path = join("..", "core" + str(wesnoth_paths.version))
    core_path = expanduser(join(wesnoth_dir, "data"))
    wesnoth_dir = expanduser(wesnoth_dir)
    wesnoth_exe = expanduser(wesnoth_exe)
    userdata_path = expanduser(userdata_path)
    input_path = expanduser(input_path)
    addon_out_path = expanduser(addon_out_path)
    core_out_path = expanduser(core_out_path)

    # call([wesnoth_exe, "--data-dir", wesnoth_dir, "--preprocess-defines", preprocess_defines, "-p", core_path,
    #       core_out_path, "--preprocess-output-macros"])
    # if wesnoth_paths.isWindows():
    #     log_files = printNewLogFiles(log_path, log_files)

    call([wesnoth_exe, "--data-dir", wesnoth_dir, "--userdata-dir", userdata_path, "--preprocess-defines",
          preprocess_defines, "-p", input_path,
          addon_out_path])
    if wesnoth_paths.isWindows():
        log_files = printNewLogFiles(log_path, log_files)


if __name__ == '__main__':
    preprocess_addon("Ageless_Era")
