from enigma import properties
from enigma.engine.swapper import Reflector
from enigma.properties.alphabet import AlphabetSettings


class ReflectorSettings:
    __REFLECTOR_KEY = "REFLECTOR"

    def __init__(self, reflector_json_file_path: str = "ReflectorProperties.JSON"):
        properties.FileProcessor.create_file_if_not_exists(reflector_json_file_path, check_json=True)
        self.__REFLECTOR_JSON_FILE_PATH = reflector_json_file_path

    def __get_pairs_dict(self) -> dict[str, str]:
        settings = properties.FileProcessor.get_dict_from_json(self.__REFLECTOR_JSON_FILE_PATH)
        if self.__REFLECTOR_KEY not in settings:
            raise KeyError("Reflector settings not set yet...")
        return dict(settings[self.__REFLECTOR_KEY])

    def save_pair(self, pair: tuple[str, str]):
        alphabet = AlphabetSettings(self.__REFLECTOR_JSON_FILE_PATH).alphabet
        x, y = pair
        x, y = x[0], y[0]
        if not (x in alphabet and y in alphabet):
            raise ValueError("Invalid chars for ReflectorSettings, you can use only from alphabet...")
        try:
            pairs_dict = self.__get_pairs_dict()
        except KeyError:
            pairs_dict = dict()
        if x in pairs_dict or y in pairs_dict:
            raise KeyError("Char already in ReflectorSettings, it can be used only once...")
        pairs_dict[x] = y
        pairs_dict[y] = x

        settings = properties.FileProcessor.get_dict_from_json(self.__REFLECTOR_JSON_FILE_PATH)
        settings[self.__REFLECTOR_KEY] = pairs_dict
        properties.FileProcessor.save_dict_to_json(self.__REFLECTOR_JSON_FILE_PATH, settings)

    @property
    def pairs(self) -> tuple[tuple[str, str]]:
        pairs_dict = self.__get_pairs_dict()
        result = []
        used = set()
        for x, y in pairs_dict.items():
            if x in used or y in used:
                continue
            result.append((x, y))
            used.add(x)
            used.add(y)
        return tuple(result)

    def clean(self):
        settings = properties.FileProcessor.get_dict_from_json(self.__REFLECTOR_JSON_FILE_PATH)
        try:
            del settings[self.__REFLECTOR_KEY]
            properties.FileProcessor.save_dict_to_json(self.__REFLECTOR_JSON_FILE_PATH, settings)
        except KeyError:
            pass

    @property
    def reflector_obj(self) -> Reflector:
        alphabet = AlphabetSettings(self.__REFLECTOR_JSON_FILE_PATH).alphabet
        return Reflector(*self.pairs, alphabet=alphabet)
