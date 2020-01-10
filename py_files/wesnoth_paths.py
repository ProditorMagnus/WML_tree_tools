import os

version = 14


def isWindows():
    return os.name == 'nt'


def getWesnothDir():
    if version == 14 and not isWindows():
        return r"~/wesnoth/wesnoth-lobby"
    if version == 14 and isWindows():
        return r"C:\Program Files (x86)\Steam\steamapps\common\wesnoth"
    if version == 15 and isWindows():
        return r"C:\Users\Ravana\games\Battle for Wesnoth 1.15.2"


def getWesnothExe():
    if version == 14 and not isWindows():
        return r"~/wesnoth/wesnoth-lobby/wesnoth"
    if version == 14 and isWindows():
        return r"C:\Program Files (x86)\Steam\steamapps\common\wesnoth\wesnoth.exe"
    if version == 15 and isWindows():
        return r"C:\Users\Ravana\games\Battle for Wesnoth 1.15.2\wesnoth.exe"


def getUserdataDir():
    if version == 14 and not isWindows():
        return r"~/wesnoth/userdata_1_14"
    if version == 14 and isWindows():
        return r"C:\Users\Ravana\Documents\My Games\Wesnoth1.14"
    if version == 15 and isWindows():
        return r"C:\Users\Ravana\Documents\My Games\Wesnoth1.15"
