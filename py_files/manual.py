#!/usr/bin/python3
from os.path import join

import rav_parser

units = ["", "", "", "", "", ""]

blacklisted_units = set("""AE_agl_steelhive_Lightshifter
AE_arc_khthon_Terrapin_Hiding
AE_mag_Walking_Corpse
AE_mrc_oracles_Scholar
AE_arc_khthon_Bone_Snapper_Hiding
AE_arc_khthon_Land_Tortoise_Hiding
AE_efm_dalefolk_shifter
AE_efm_dalefolk_shifter_Bear
AE_efm_dalefolk_shifter_Beaver
AE_efm_dalefolk_shifter_Goat
AE_efm_dalefolk_shifter_Human
AE_efm_dalefolk_shifter_Warthog
AE_efm_dalefolk_shifter_Wolf
AE_feu_khaganate_Shieldbearer
AE_arc_khthon_Rock_Back_Hiding
AE_arc_khthon_Rock_Snapper_Hiding
AE_efm_dalefolk_Wilderman
AE_efm_dalefolk_Wilderman_Bear
AE_efm_dalefolk_Wilderman_Beaver
AE_efm_dalefolk_Wilderman_Goat
AE_efm_dalefolk_Wilderman_Human
AE_efm_dalefolk_Wilderman_Warthog
AE_efm_dalefolk_Wilderman_Wolf
AE_mrc_Blight_Fleshpool
AE_feu_khaganate_Rigid
AE_feu_khaganate_Stoic
AE_arc_khthon_Adamantine_Hiding
AE_mag_Runemaster_Protected
AE_mag_Goblin_Kamikaze
AE_mrc_fanatics_Martyr
AE_efm_imperialists_Sapper
AE_mag_bug_3827
""".split())


def write(level, text):
    units[level] += text


def slice(level, start=0, end=-1):
    units[level] = units[level][start:end]


def result_function(description, path, attributes):
    unit_id = attributes[1]["id"]
    if unit_id in blacklisted_units:
        return
    write(current_level, '\t"{}",\n'.format(unit_id))


addonId = "Ageless_Era"
root_node = rav_parser.load_root_node(addonId)

for current_level, var_name in [(2, "ORM.unit.level_two")]:
    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/level=={}".format(current_level)), rav_parser.parse_wml_query("[units]/[unit_type]/[attack]/[specials]/[chance_to_hit]/id==magical")]
    output_keys = ["id"]

    write(current_level, var_name + ' = {\n')
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, result_function)
    slice(current_level, 0, -2)
    write(current_level, '}')

with open("sevu_mages.lua", "w", encoding="utf8") as f:
    f.write("--<<\n")
    f.write("-- This file is regenerated for each ageless release\n")
    for u in units:
        f.write(u)
        f.write("\n")
    f.write("-->>\n")

