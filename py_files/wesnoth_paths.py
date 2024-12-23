import os

version = 19


def isWindows():
    return os.name == 'nt'


def getWesnothDir():
    if version == 19 and isWindows():
        return r"C:\Users\Ravana\games\battle-for-wesnoth-1.19.7"
    if version == 18 and isWindows():
        return r"C:\Program Files (x86)\Steam\steamapps\common\wesnoth"


def getWesnothExe():
    if version == 19 and isWindows():
        return r"C:\Users\Ravana\games\battle-for-wesnoth-1.19.7\wesnoth.exe"
    if version == 18 and isWindows():
        return r"C:\Program Files (x86)\Steam\steamapps\common\wesnoth\wesnoth.exe"


def getUserdataDir():
    # intentionally 1.18
    if version == 19 and isWindows():
        return r"C:\Users\Ravana\Documents\My Games\Wesnoth1.18"
    if version == 18 and isWindows():
        return r"C:\Users\Ravana\Documents\My Games\Wesnoth1.18"
