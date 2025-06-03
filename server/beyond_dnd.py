import os
import requests
import logging
from json import dumps, loads
from typing import List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Constants
HOLY_SYMBOL = 'holy symbol'
ARCANE_FOCUS = 'arcane focus'
DRUIDIC_FOCUS = 'druidic focus'
SPELL_COMPONENT_PREFIX = 'SMC'
CONSUME_TEXT = 'consume'
GP_COST_TEXT = 'gp'


class BeyondDnDAPIError(Exception):
    pass


class BeyondDnD:
    # Added custom item param in case, to prevent changes in future if we use homebrew/custom
    _BASE_URL = 'https://character-service.dndbeyond.com/character/v5/character/{}?includeCustomItems=true'
    _LOCAL_CHARACTER_DATA_FILE = 'local_character_data.json'
    _LOCAL_CHARACTER_IDS_FILE = 'local_character_ids.json'

    def get_bdnd_all_character_data(
        self, char_ids: List[str] = None, update_one: bool = False, force_update: bool = False
    ) -> dict:
        # If getting char_ids, get new data anyway
        if char_ids:
            char_data = self.__get_all_character_data(char_ids)
            # If only updating a single character, don't overwrite the ID file
            if not update_one:
                self.__save_local_file(char_ids, self._LOCAL_CHARACTER_IDS_FILE)
            self.__save_local_file(char_data, self._LOCAL_CHARACTER_DATA_FILE)
            return char_data
        else:
            character_data = self.__load_local_file_if_exists(self._LOCAL_CHARACTER_DATA_FILE)
            if character_data and not force_update:
                return character_data
            local_char_ids = self.__load_local_file_if_exists(self._LOCAL_CHARACTER_IDS_FILE)
            if local_char_ids:
                char_data = self.__get_all_character_data(local_char_ids)
                self.__save_local_file(char_data, self._LOCAL_CHARACTER_DATA_FILE)
                return char_data
        raise BeyondDnDAPIError("Characters ids were not provided and the default file was not found.")

    def __get_all_character_data(self, char_ids: List[str]) -> dict:
        character_data = {}
        for char_id in char_ids:
            resp = self.__get_bdnd_character_data(char_id)
            data = self.__format_character_data(resp, char_id)
            character_data[char_id] = data
        return character_data

    @staticmethod
    def __save_local_file(data, file):
        cur_dir = os.getcwd() # ["146993912", "144768530"]
        file_path = cur_dir+'/tmp'
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)
        with open(file_path+'/'+file, 'w') as f:
            body = dumps(data)
            f.write(body)
            f.close()

    @staticmethod
    def __load_local_file_if_exists(save_path):
        cur_dir = os.getcwd()
        file_path = Path(cur_dir+'/tmp/'+save_path)
        if file_path.exists():
            with open(file_path, 'r') as f:
                return loads(f.read())
        return None

    def __get_bdnd_character_data(self, char_id: str):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        resp = requests.get(headers=headers, url=self._BASE_URL.format(char_id))
        if resp.status_code >= 300:
            logger.error(dumps({
                "message": "Shit broke, debug it",
                "characterId": char_id,
                "error": resp.text,
                "statusCode": resp.status_code
            }))
            raise BeyondDnDAPIError("Something didn't work")
        return resp.json()

    def __format_character_data(self, data: dict, char_id: str) -> (str, dict):
        if not data:
            raise BeyondDnDAPIError(f'No Character test_data found for characterId: {char_id}')
        char_data = data.get('data', {})
        name = char_data.get("name")
        inventory_items = char_data.get("inventory")
        custom_items = char_data.get("customItems")
        counted_items, counted_custom_items, focus = self.__count_inventory_items(inventory_items, custom_items)
        spells = self.__build_character_spell_list(char_data)
        return {
            'name': name,
            'spells': spells,
            'custom_items': counted_custom_items,
            'inventory': counted_items,
            'focus': focus
        }

    def __build_character_spell_list(self, data: dict) -> dict:
        """
        Spells can come from multiple places in test_data:
            test_data.spells.race [] - Spells from characters race/species
            test_data.spells.class [] - Spells specific spells
            test_data.spells.item [] - Spells that come from items, I think this is unimportant.Typically, the options of effects
            test_data.classSpells [] - Spells / cantrips chosen when leveling
        """
        parsed_spells = {}
        spells = data.get('spells', {})
        class_leveling_spells = []
        for cls_spells in data.get('classSpells', []):
            class_leveling_spells += cls_spells.get('spells', [])
        race_spells = spells.get('race', [])
        class_specific_spells = spells.get('class', [])

        # all spells seem to have the same schema, combining all sources for one loop
        all_spells = class_leveling_spells + race_spells + class_specific_spells
        for spell in all_spells:
            spell_data = spell.get('definition', {})
            name = spell_data.get('name')
            component_desc = spell_data.get('componentsDescription')
            spell_description = self.parse_spell_description(component_desc)
            parsed_spells[name] = spell_description
        return parsed_spells

    @staticmethod
    def parse_spell_description(description: Optional[str]) -> dict:
        if not description:
            return {
                'componentsDescription': '',
                'componentsAreConsumed': False,
                'componentsHaveCost': False,
                'focusWillWork': True,  # This is just set for true, nothing is needed but whatever
            }
        found_consume_text = CONSUME_TEXT.lower() in description.lower()
        found_gp_cost_text = GP_COST_TEXT.lower() in description.lower()
        return {
            'componentsDescription': description,
            'componentsAreConsumed': found_consume_text,
            'componentsHaveCost': found_gp_cost_text,
            'focusWillWork': not found_consume_text and not found_gp_cost_text
        }

    def __count_inventory_items(self, inventory_items: List[dict], custom_items: List[dict]) -> (dict, dict, Optional[dict]):
        # Returns item counts, custom item counts, and focus item if found (None otherwise)
        focus = None
        counts = {}
        custom_counts = {}
        for item in inventory_items:
            item_data = item.get('definition', {})
            name = item_data.get('name')
            if not name:
                # DON'T WASTE MY TIME POINTLESS ITEM OR BAD DATA
                continue
            subtype = item_data.get('subType')
            if self.__item_is_focus_item(subtype):
                focus = item_data
            quantity = item_data.get('quantity', 1)  # default to 1, assuming this item is present and thus 1
            if name not in counts:
                counts[name] = quantity
            else:
                counts[name] = quantity + counts[name]

        for item in custom_items:
            # Can add a focus check here if we add something custom
            name = item.get('name')
            if not name or not name.startswith(SPELL_COMPONENT_PREFIX):
                continue
            splits = name.split(':')
            if len(splits) < 3:  # if we get rid of prefix, this will need to be changed.
                continue
            # IF FOR SOME REASON THERE ARE TWO ITEMS OF THE SAME TYPE, WE ARE NOT ADDING RN. IT WILL BE OVERWRITTEN
            custom_counts[splits[1]] = splits[2]
        return counts, custom_counts, focus

    @staticmethod
    def __item_is_focus_item(subtype: str = None) -> bool:
        if not subtype:
            return False
        return subtype.lower() in {HOLY_SYMBOL, ARCANE_FOCUS, DRUIDIC_FOCUS}

    @staticmethod
    def __format_focus_data(focus_data: dict) -> dict:
        return {
            'name': focus_data.get('name', ''),
            'type': focus_data.get('type', ''),
            'subType': focus_data.get('subType', ''),
            'description': focus_data.get('description', '')
        }
