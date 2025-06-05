import os
import shutil
import requests
import logging
from http import HTTPStatus
from json import dumps, loads
from typing import List, Optional, Tuple
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
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


class BeyondDnDClient:
    # TODO: If useful, in future can store character ids by campaign_id to manage multiple campaigns.
    # Added custom item param in case, to prevent changes in future if we use homebrew/custom
    _BASE_URL = 'https://character-service.dndbeyond.com/character/v5/character/{}?includeCustomItems=true'
    _LOCAL_CHARACTER_DATA_FILE = 'local_character_data.json'

    def get_all_characters_data(self, char_ids: Optional[List[str]] = None, force_update: bool = False) -> dict:
        if not force_update:
            character_data = self.__load_local_file_if_exists(self._LOCAL_CHARACTER_DATA_FILE)
            if character_data:
                # return whatever data was previously saved
                return character_data
        dungeon_data = self.__get_all_character_data(char_ids)
        if dungeon_data:
            self.__save_local_file(dungeon_data, self._LOCAL_CHARACTER_DATA_FILE)
            return dungeon_data
        raise BeyondDnDAPIError(
            "Characters ids were not provided and/or the default file was not found.", HTTPStatus.BAD_REQUEST
        )

    def get_one_characters_data(self, char_id: str, force_update: bool = False):
        if force_update:
            dungeon_data = self.__get_one_characters_data(char_id)
            self.__update_local_file_if_exists(
                {'characters': {char_id: dungeon_data}}, self._LOCAL_CHARACTER_DATA_FILE
            )
            return dungeon_data
        else:
            # Check if the data exists locally
            all_character_data = self.__load_local_file_if_exists(self._LOCAL_CHARACTER_DATA_FILE)
            if all_character_data:
                character_data = all_character_data.get('characters', {})
                if char_id in character_data: return character_data[char_id]
            # If no data stored locally, do not retrieve from API. Prefer bulk ID's to prevent random characters
            #   from being added.
        raise BeyondDnDAPIError(
            message=f'No local data was found for character_id: {char_id}. '
                    f'Try again with force_update or update all characters',
            status_code=HTTPStatus.NOT_FOUND,
        )

    @staticmethod
    def delete_all_cached_character_data():
        cur_dir = os.getcwd()
        directory_path = Path(cur_dir + '/tmp/')
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)

    def __get_one_characters_data(self, char_id: str) -> dict:
        resp = self.__get_bdnd_character_data(char_id)
        resp_data = resp.get('data', {})
        return self.__format_character_data(resp_data, char_id)

    def __get_all_character_data(self, char_ids: List[str]) -> dict:
        all_character_data = {}
        campaign_data = None
        for char_id in char_ids:
            resp = self.__get_bdnd_character_data(char_id)
            resp_data = resp.get('data', {})
            if not campaign_data:
                # only need to get this data once, ignore once successful
                campaign_data = self.__extract_campaign_metadata(resp_data.get('campaign'))
            character_data = self.__format_character_data(resp_data, char_id)
            all_character_data[char_id] = character_data
        return {
            "characters": all_character_data,
            "campaign": campaign_data
        }

    @staticmethod
    def __save_local_file(data, file: str):
        cur_dir = os.getcwd()
        file_path = cur_dir+'/tmp/'
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)
        with open(file_path+file, 'w') as f:
            body = dumps(data)
            f.write(body)
            f.close()

    @staticmethod
    def __load_local_file_if_exists(save_path: str):
        cur_dir = os.getcwd()
        file_path = Path(cur_dir + '/tmp/' + save_path)
        if file_path.exists():
            with open(file_path, 'r') as f:
                return loads(f.read())
        return None

    def __update_local_file_if_exists(self, data: dict, file: str) -> bool:
        local_data = self.__load_local_file_if_exists(file)
        if local_data and isinstance(local_data, dict):
            local_data.update(data)
            self.__save_local_file(local_data, file)
            return True
        return False

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
            raise BeyondDnDAPIError(f"BeyondDnD API failure, ensure character profile is set to Public and "
                                    f"that the ID was entered correctly. Error: {resp.text}", resp.status_code)
        return resp.json()

    def __format_character_data(self, char_data: dict, char_id: str) -> dict:
        if not char_data:
            raise BeyondDnDAPIError(
                f'No Character Data found for characterId: {char_id}', HTTPStatus.INTERNAL_SERVER_ERROR
            )
        name = char_data.get("name")
        inventory_items = char_data.get("inventory", [])
        custom_items = char_data.get("customItems", [])
        counted_items, counted_custom_items, focus = self.__count_inventory_items(inventory_items, custom_items)
        spells = self.__build_character_spell_list(char_data)
        return {
            'name': name,
            'spells': spells,
            'custom_items': counted_custom_items,
            'inventory': counted_items,
            'focus': focus,
        }

    def __build_character_spell_list(self, data: dict) -> List[dict]:
        """
        Spells can come from multiple places in test_data:
            test_data.spells.race [] - Spells from characters race/species
            test_data.spells.class [] - Spells specific spells
            test_data.spells.item [] - Spells that come from items, I think this is unimportant.Typically, the options of effects
            test_data.classSpells [] - Spells / cantrips chosen when leveling
        """
        parsed_spells = []
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
            spell_data = self.__parse_spell_description(name, component_desc)
            parsed_spells.append(spell_data)
        return parsed_spells

    @staticmethod
    def __parse_spell_description(name: str, description: Optional[str]) -> dict:
        if not description:
            return {
                'name': name,
                'componentsDescription': '',
                'componentsAreConsumed': False,
                'componentsHaveCost': False,
                'focusWillWork': True,  # This is just set for true, nothing is needed but whatever
            }
        found_consume_text = CONSUME_TEXT.lower() in description.lower()
        found_gp_cost_text = GP_COST_TEXT.lower() in description.lower()
        return {
            'name': name,
            'componentsDescription': description,
            'componentsAreConsumed': found_consume_text,
            'componentsHaveCost': found_gp_cost_text,
            'focusWillWork': not found_consume_text and not found_gp_cost_text
        }

    def __count_inventory_items(self, inventory_items: List[dict], custom_items: List[dict]) -> Tuple[dict, dict, Optional[dict]]:
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
                focus = self.__extract_focus_data(item_data)
            quantity = item.get('quantity', 1)  # default to 1, assuming this item is present and thus 1
            if name not in counts:
                counts[name] = quantity
            else:
                counts[name] = quantity + counts[name]

        for item in custom_items:
            # Note: Can add a focus check here if we add something custom
            name = item.get('name')
            if not name or not name.startswith(SPELL_COMPONENT_PREFIX):
                continue
            splits = name.split(':')
            if len(splits) < 3:  # if we get rid of 'SMC' prefix, this will need to be changed.
                continue
            # NOTE: If there are more than 1 custom item with the same name, the last found will be the only displayed.
            #  If for some reason we need multiple entries, that will require a code change. But seriously, just update
            #  the one custom item asshole.
            custom_counts[splits[1]] = splits[2]
        return counts, custom_counts, focus

    @staticmethod
    def __item_is_focus_item(subtype: Optional[str] = None) -> bool:
        if not subtype:
            return False
        return subtype.lower() in {HOLY_SYMBOL, ARCANE_FOCUS, DRUIDIC_FOCUS}

    @staticmethod
    def __extract_focus_data(focus_data: dict) -> dict:
        return {
            'name': focus_data.get('name', ''),
            'type': focus_data.get('type', ''),
            'subType': focus_data.get('subType', ''),
            'description': focus_data.get('description', '')
        }

    @staticmethod
    def __extract_campaign_metadata(campaign_data: Optional[dict]) -> Optional[dict]:
        if not campaign_data:
            return None
        return {
            "name": campaign_data.get('name', ''),
            "description": campaign_data.get('description', ''),
            "dmUsername": campaign_data.get('dmUsername', '')
        }
