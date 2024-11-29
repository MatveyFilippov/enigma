import json
import os
import random
import string
from typing import Any
from enigma.properties.rotor import RotorsSettings
from enigma.properties.alphabet import AlphabetSettings
from enigma.properties.reflector import ReflectorSettings


class FileProcessor:
    @staticmethod
    def create_file_if_not_exists(filepath: str, check_json=False):
        if os.path.exists(filepath) and os.path.isfile(filepath):
            if not check_json:
                return
            if FileProcessor.is_json_file(filepath):
                return
        parent_dir = os.path.dirname(filepath)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)
        with open(filepath, "w") as json_file:
            json.dump(dict(), json_file)

    @staticmethod
    def is_json_file(filepath: str) -> bool:
        try:
            with open(filepath, "r") as json_file:
                dict(json.load(json_file))
        except Exception:
            return False
        return True

    @staticmethod
    def get_dict_from_json(json_filepath: str) -> dict[str, Any]:
        if not FileProcessor.is_json_file(json_filepath):
            raise FileNotFoundError("RotorsSettings not exists or damaged")
        with open(json_filepath, "r", encoding="UTF-8") as json_file:
            return dict(json.load(json_file))

    @staticmethod
    def save_dict_to_json(json_filepath: str, to_dump: dict[str, Any]):
        FileProcessor.create_file_if_not_exists(json_filepath)
        with open(json_filepath, "w", encoding="UTF-8") as json_file:
            json.dump(to_dump, json_file, ensure_ascii=False)


class EnigmaProperties:
    def __init__(self, enigma_json_file_path: str = "EnigmaProperties.JSON"):
        FileProcessor.create_file_if_not_exists(enigma_json_file_path, check_json=True)
        self.__ENIGMA_JSON_FILE_PATH = enigma_json_file_path

        self.ROTORS_SETTINGS = RotorsSettings(self.__ENIGMA_JSON_FILE_PATH)
        self.ALPHABET_SETTINGS = AlphabetSettings(self.__ENIGMA_JSON_FILE_PATH)
        self.REFLECTOR_SETTINGS = ReflectorSettings(self.__ENIGMA_JSON_FILE_PATH)

    def create_random_alphabet(self):
        available_for_new_alphabet = string.digits + string.ascii_uppercase
        new_alphabet_len = random.randint(2, len(available_for_new_alphabet))
        if new_alphabet_len % 2 != 0:
            new_alphabet_len -= 1
        new_alphabet = set()
        while len(new_alphabet) < new_alphabet_len:
            new_alphabet.add(random.choice(available_for_new_alphabet))
        self.ALPHABET_SETTINGS.alphabet = "".join(new_alphabet)

    def create_random_rotors(self, rotors_qty: int | None = None):
        if not rotors_qty:
            rotors_qty = random.randint(2, 5)
        alphabet_const = self.ALPHABET_SETTINGS.alphabet
        for rotor_id in range(1, rotors_qty+1):
            temp_alphabet = list(alphabet_const)
            random.shuffle(temp_alphabet)
            self.ROTORS_SETTINGS.save_new_rotor_wiring(rotor_id=rotor_id, wiring="".join(temp_alphabet))

    def create_random_reflector(self):
        alphabet_list = list(self.ALPHABET_SETTINGS.alphabet)
        random.shuffle(alphabet_list)
        for _ in range(0, len(alphabet_list), 2):
            self.REFLECTOR_SETTINGS.save_pair(
                (alphabet_list.pop(), alphabet_list.pop())
            )

    def fill_settings_by_random_values(self):
        FileProcessor.save_dict_to_json(self.__ENIGMA_JSON_FILE_PATH, dict())
        self.create_random_alphabet()
        self.create_random_rotors()
        self.create_random_reflector()
