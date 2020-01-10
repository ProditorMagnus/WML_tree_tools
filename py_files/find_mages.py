from collections import defaultdict

import rav_parser
from typing import List, Dict

Attributes = Dict[str, str]

addonId = "Ageless_Era"
root_node = rav_parser.load_root_node(addonId, False)


def find_mages():
    mages = set()

    def mage_find_function(description, path, attributes):
        unit_id = attributes[1]["id"]
        if "level" not in attributes[1]:
            print(unit_id, "has no level")
            return
        unit_level = int(attributes[1]["level"])
        weapon_range = attributes[2]["range"]
        if unit_level == 2 and weapon_range == "ranged":
            mages.add(unit_id)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[attack]/[specials]/[chance_to_hit]/id==magical")]
    output_keys = ["id", "type", "level", "range"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, mage_find_function)
    print(sorted(mages))


def check_damage_types():
    mage_attacks = defaultdict(int)
    nonmage_attacks = defaultdict(int)

    def nonmage_function(description, path, attributes):
        unit_id = attributes[1]["id"]
        if unit_id not in mages:
            return
        strikes = int(attributes[2]["number"])
        damage = int(attributes[2]["damage"])
        nonmage_attacks[unit_id] = max(nonmage_attacks[unit_id], strikes * damage)

    def mage_function(description, path, attributes):
        unit_id = attributes[1]["id"]
        if unit_id not in mages:
            return
        strikes = int(attributes[2]["number"])
        damage = int(attributes[2]["damage"])
        if "level" not in attributes[1]:
            print(unit_id, "has no level")
            return
        if "hide_help" in attributes[1]:
            print(unit_id, "has hide_help attribute")
            return
        unit_level = int(attributes[1]["level"])
        weapon_range = attributes[2]["range"]
        if unit_level == 2 and weapon_range == "ranged":
            mage_attacks[unit_id] = max(mage_attacks[unit_id], strikes * damage)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[attack]")]
    output_keys = ["id", "damage", "number", "hide_help", "level", "range"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, nonmage_function)

    parsed_query = [rav_parser.parse_wml_query("[units]/[unit_type]/[attack]/[specials]/[chance_to_hit]/id==magical")]
    output_keys = ["id", "damage", "number", "hide_help", "level", "range"]
    rav_parser.find_from_wml(root_node, [], parsed_query, output_keys, mage_function)

    for unit in nonmage_attacks:
        if mage_attacks[unit] == nonmage_attacks[unit]:
            print(unit)


mages = ['AE_agl_desert_elves_Druid', 'AE_agl_frozen_frost_mage', 'AE_agl_frozen_frost_witch', 'AE_agl_yokai_Banshee',
         'AE_agl_yokai_Feyborn_Witch', 'AE_agl_yokai_Kitsune', 'AE_agl_yokai_Phantom', 'AE_agl_yokai_Tengu',
         'AE_arc_despair_Widow_in_White', 'AE_arc_menagerie_Blue_Mage', 'AE_arc_orcs_Vagrant', 'AE_arc_orcs_Wanderer',
         'AE_arc_phantom_Mummy_Noble', 'AE_arc_primeval_Primevalist_Celebrant', 'AE_arc_primeval_Primevalist_Monk',
         'AE_arc_south_seas_Gale', 'AE_arc_south_seas_Seahag', 'AE_bem_anakes_Hierophant', 'AE_bem_anakes_Spellcaster',
         'AE_bem_wood_warriors_Woods_Druid', 'AE_chs_aragwaith_Wizard', 'AE_chs_chaos_empire_Demon_Shapeshifter',
         'AE_chs_chaos_empire_Magus', 'AE_chs_elementals_Summoner_of_Earth', 'AE_chs_elementals_Summoner_of_Fire',
         'AE_chs_elementals_Summoner_of_Water', 'AE_chs_elementals_Summoner_of_Wind',
         'AE_chs_quenoth_Quenoth_Moon_Enchantress', 'AE_chs_quenoth_Quenoth_Sun_Enchantress',
         'AE_chs_sylvians_Elvish_Ascetic', 'AE_chs_sylvians_Fire_Faerie', 'AE_chs_sylvians_Night_Nymph',
         'AE_chs_wild_humans_Shadow_Mage', 'AE_efm_dalefolk_Beacon', 'AE_efm_darklanders_Wrath_of_the_Gods',
         'AE_efm_freemen_Howler', 'AE_efm_highlanders_Shaman', 'AE_efm_highlanders_Warlock',
         'AE_efm_pygmies_Toad_Breath', 'AE_efm_pygmies_Wyrd', 'AE_efm_whites_Storm_Witch', 'AE_ele_Centaur_Apprentice',
         'AE_ele_Centaur_Priestess', 'AE_ele_Fallen_Asperser', 'AE_ele_Skeletal_Corpse_Burner',
         'AE_ele_Skeletal_Lich_Lord', 'AE_ele_Skeletal_Sorceress', 'AE_ext_chaos_Magus', 'AE_ext_dark_elves_Sorcerer',
         'AE_ext_dark_elves_Sorceress', 'AE_ext_northerns_Troll_Shaman', 'AE_ext_outlaws_Shadow_Mage',
         'AE_ext_outlaws_Witch', 'AE_feu_ceresians_Deacon', 'AE_feu_ceresians_Monk', 'AE_feu_ceresians_Order_Knight',
         'AE_feu_high_elves_Enchantress', 'AE_feu_high_elves_Feyblade', 'AE_feu_khaganate_Icewind_Drover',
         'AE_fut_Nordhris_Tribal_Sage', 'AE_fut_brungar_Ice_Apprentice', 'AE_fut_brungar_Wave_Rider',
         'AE_fut_welkin_Battle_Sage', 'AE_fut_welkin_Elder_Sage', 'AE_fut_welkin_Pyroation', 'AE_fut_welkin_Quickdraw',
         'AE_fut_welkin_Shadow_Raider', 'AE_fut_welkin_Talon_Warrior', 'AE_fut_welkin_Whirlwind',
         'AE_imp_Arendians_Shaman', 'AE_imp_Cavernei_Observer', 'AE_imp_Issaelfr_Mistral_Glacialist',
         'AE_imp_Marauders_Seeress', 'AE_imp_Marauders_Shieldmaiden', 'AE_imp_Sidhe_Ancestor', 'AE_imp_Sidhe_Warmage',
         'AE_imp_Sidhe_Windlasher', 'AE_mag_Black_Mage', 'AE_mag_Child_of_Light', 'AE_mag_Clan_Leader', 'AE_mag_Cleric',
         'AE_mag_Commander', 'AE_mag_Corrupted_Shaman', 'AE_mag_Cyclops_Necromancer', 'AE_mag_Dark_Portal',
         'AE_mag_Dark_Wizard', 'AE_mag_Dispeller', 'AE_mag_Efreet', 'AE_mag_Elemental_Archer', 'AE_mag_Fire_Avatar',
         'AE_mag_Goblin_Druid', 'AE_mag_Golem_Boss', 'AE_mag_Great_Jinn', 'AE_mag_Great_Witch', 'AE_mag_Inspired',
         'AE_mag_Kharos_Warbanner', 'AE_mag_Legendary_Cyclops', 'AE_mag_Mage_of_Air', 'AE_mag_Mage_of_Fire',
         'AE_mag_Mage_of_Water', 'AE_mag_Perfect_Drone', 'AE_mag_Red_Salamander', 'AE_mag_RhamiDatu', 'AE_mag_RhamiKai',
         'AE_mag_Runesmith', 'AE_mag_Sculptor', 'AE_mag_Shamanistic_Toad', 'AE_mag_Silver_Warrior', 'AE_mag_Sorcerer',
         'AE_mag_Storm_Sphere', 'AE_mag_Troll_Fire_Wizard', 'AE_mag_Troll_Warbanner', 'AE_mag_War_Mage',
         'AE_mie_centaur_augur', 'AE_mie_cornur_warlock', 'AE_mie_sylvan_faerie', 'AE_mie_sylvan_shadow_faerie',
         'AE_mie_thelian_ancestor', 'AE_mie_thelian_blood_shaman', 'AE_mie_thelian_druid', 'AE_mie_vampire_savant',
         'AE_mrc_enchanters_Arcane_Rune_Transcriber', 'AE_mrc_enchanters_Clearbow',
         'AE_mrc_enchanters_Elemental_Rune_Interpreter', 'AE_mrc_enchanters_Rune_Fire_Specialist',
         'AE_mrc_equestrians_Mageknight', 'AE_mrc_equestrians_Troubadour', 'AE_mrc_fanatics_Master_Genie',
         'AE_mrc_holy_order_Mage', 'AE_mrc_holy_order_Scholar', 'AE_mrc_infernai_Master_Ifreet',
         'AE_mrc_mercenaries_Isolated_Mage', 'AE_mrc_mercenaries_Warrior_Mage', 'AE_mrc_oracles_Magus',
         'AE_mrc_oracles_Necromantic', 'AE_mrc_oracles_Occultist', 'AE_mrc_oracles_Prophet', 'AE_mrc_oracles_Warlock',
         'AE_mrc_refugees_Purifier', 'AE_mrc_tribe_Medicineman', 'AE_mrc_tribe_Witchdoctor', 'AE_myh_Blasphemists',
         'AE_myh_Blood_Manipulator', 'AE_myh_Flesh_Artisan', 'AE_myh_Great_Wizard', 'AE_myh_Mystic',
         'AE_myh_Pathfinder', 'AE_myh_Savant', 'AE_myh_Silver_Unicorn', 'AE_myh_Skyrunner', 'AE_myh_Therian_Mage',
         'AE_myh_Therian_Shaman', 'AE_myh_Thunderbird', 'AE_rhy_aq_Blue_Mage', 'AE_rhy_de_Elvish_Ship',
         'AE_rhy_de_Shadowpriest', 'AE_rhy_de_Shadowprincess', 'AE_rhy_de_Spiderpriest', 'AE_rhy_dw_Runemage',
         'AE_rhy_ey_Healer', 'AE_rhy_ey_Lord', 'AE_rhy_ey_Nymph', 'AE_rhy_ey_Sorcerer', 'AE_rhy_ey_Waterfairy',
         'AE_rhy_fd_Gnome_Knight', 'AE_rhy_fd_Gnome_Luck', 'AE_rhy_fh_Healer', 'AE_rhy_fh_Mage', 'AE_rhy_lz_Cleric',
         'AE_rhy_lz_Monk', 'AE_rhy_ma_Battlemage', 'AE_rhy_ma_Sorcerer', 'AE_rhy_ma_Warmonk', 'AE_rhy_mh_Wise',
         'AE_rhy_tr_Dimension', 'AE_rhy_tr_Lightning', 'AE_rhy_tr_Matter', 'AE_rhy_vx_Priest', 'AE_rhy_vx_Sorceress',
         'AE_stf_eltireans_Bishop_of_Eltire', 'AE_stf_eltireans_Hydromancer', 'AE_stf_eltireans_Lightbringer',
         'AE_stf_eltireans_Pyromancer', 'AE_stf_free_saurians_Elementalist', 'AE_stf_free_saurians_Healer',
         'AE_stf_free_saurians_Mystic', 'AE_stf_free_saurians_Soulmage', 'AE_stf_minotaurs_Mystic',
         'AE_stf_minotaurs_Warlock']
check_damage_types()
