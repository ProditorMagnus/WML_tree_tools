import os

version = 18


def isWindows():
    return os.name == 'nt'


def getWesnothDir():
    if version == 18 and isWindows():
        return r"C:\Program Files (x86)\Steam\steamapps\common\wesnoth"
    if version == 17 and isWindows():
        return r"C:\Users\Ravana\games\battle-for-wesnoth-1.17.24"


def getWesnothExe():
    if version == 18 and isWindows():
        return r"C:\Program Files (x86)\Steam\steamapps\common\wesnoth\wesnoth.exe"
    if version == 17 and isWindows():
        return r"C:\Users\Ravana\games\battle-for-wesnoth-1.17.24\wesnoth_1_17_24.exe"


def getUserdataDir():
    if version == 18 and isWindows():
        return r"C:\Users\Ravana\Documents\My Games\Wesnoth1.18"
