import os

version = 18


def isWindows():
    return os.name == 'nt'


def getWesnothDir():
    if version == 14 and not isWindows():
        return r"~/wesnoth/wesnoth-lobby"
    if version == 15 and isWindows():
        return r"C:\Users\Ravana\games\Battle for Wesnoth 1.15.14"
    if version == 16 and isWindows():
        return r"C:\Program Files (x86)\Steam\steamapps\common\wesnoth"
    if version == 17 and isWindows():
        return r"C:\Users\Ravana\games\battle-for-wesnoth-1.17.24"
    if version == 18 and isWindows():
        return r"C:\Users\Ravana\games\battle-for-wesnoth-1.18.0"


def getWesnothExe():
    if version == 14 and not isWindows():
        return r"~/wesnoth/wesnoth-lobby/wesnoth"
    if version == 15 and isWindows():
        return r"C:\Users\Ravana\games\Battle for Wesnoth 1.15.14\wesnoth.exe"
    if version == 16 and isWindows():
        return r"C:\Program Files (x86)\Steam\steamapps\common\wesnoth\wesnoth.exe"
    if version == 17 and isWindows():
        return r"C:\Users\Ravana\games\battle-for-wesnoth-1.17.24\wesnoth_1_17_24.exe"
    if version == 18 and isWindows():
        return r"C:\Users\Ravana\games\battle-for-wesnoth-1.18.0\wesnoth_1_18_0.exe"


def getUserdataDir():
    if version == 14 and not isWindows():
        return r"~/wesnoth/userdata_1_14"
    if version == 15 and isWindows():
        return r"C:\Users\Ravana\Documents\My Games\Wesnoth1.15"
    if version == 16 and isWindows():
        return r"C:\Users\Ravana\Documents\My Games\Wesnoth1.16"
    if version == 17 and isWindows():
        return r"C:\Users\Ravana\Documents\My Games\Wesnoth1.17"
    if version == 18 and isWindows():
        return r"C:\Users\Ravana\Documents\My Games\Wesnoth1.18"
