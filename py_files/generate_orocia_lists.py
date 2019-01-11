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
    unit_id = attributes[1][0][1]
    if unit_id in blacklisted_units:
        return
    write(current_level, '\t"{}",\n'.format(unit_id))


addonId = "Ageless_Era"
root_node = rav_parser.parse_root_node(join("..", "preprocessed_addon", addonId, "_main.cfg"))

for current_level, var_name in [(0, "ORM.unit.level_zero"), (1, "ORM.unit.level_one"), (2, "ORM.unit.level_two"),
                                (3, "ORM.unit.level_three"), (4, "ORM.unit.level_four")]:
    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/level=={}".format(current_level))]
    output_keys = ["id"]

    write(current_level, var_name + ' = {\n')
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, result_function)
    slice(current_level, 0, -2)
    write(current_level, '}')

with open("data_generated_units.lua", "w", encoding="utf8") as f:
    f.write("--<<\n")
    f.write("-- This file is regenerated for each ageless release\n")
    for u in units:
        f.write(u)
        f.write("\n")
    f.write("-->>\n")

for u in ["AE_agl_frozen_frost_witch", "AE_bem_anakes_Hierophant", "AE_bem_wood_warriors_Woods_Druid",
          "AE_chs_aragwaith_Wizard", "AE_efm_highlanders_Shaman", "AE_feu_ceresians_Deacon", "AE_fut_brungar_Herbalist",
          "AE_fut_welkin_Elder_Sage", "AE_imp_Arendians_Shaman", "AE_mag_Water_Avatar", "AE_mag_Clan_Leader",
          "AE_mag_Shamanistic_Toad", "AE_mag_Child_of_Light", "AE_mag_Cleric", "AE_mag_Mage_of_Water",
          "AE_mrc_avians_Sitter", "AE_mrc_enchanters_Arcane_Rune_Transcriber", "AE_mrc_equestrians_Troubadour",
          "AE_mrc_fanatics_Master_Genie", "AE_mrc_highlanders_Combatmedic", "AE_mrc_hive_Queen",
          "AE_mrc_holy_order_Priest", "AE_mrc_infernai_Master_Ifreet", "AE_stf_free_saurians_Healer",
          "AE_stf_minotaurs_Mystic", "AE_fut_Nordhris_Witch_Doctor"]:
    if u not in units[2]:
        print("Not in level 2 units:", u)
