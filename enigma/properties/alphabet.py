from enigma import properties


class AlphabetSettings:
    __ALPHABET_KEY = "ALPHABET"

    def __init__(self, alphabet_json_file_path: str = "AlphabetProperties.JSON"):
        properties.FileProcessor.create_file_if_not_exists(alphabet_json_file_path, check_json=True)
        self.__ALPHABET_JSON_FILE_PATH = alphabet_json_file_path

    @property
    def alphabet(self) -> str:
        settings = properties.FileProcessor.get_dict_from_json(self.__ALPHABET_JSON_FILE_PATH)
        if self.__ALPHABET_KEY not in settings:
            raise KeyError("ALPHABET not set yet...")
        return settings[self.__ALPHABET_KEY].upper()

    @alphabet.setter
    def alphabet(self, _new: str):
        if len(_new) % 2 != 0:
            raise ValueError("Enigma alphabet qty must be even")
        _new = "".join(sorted(list(set(_new))))
        settings = properties.FileProcessor.get_dict_from_json(self.__ALPHABET_JSON_FILE_PATH)
        settings[self.__ALPHABET_KEY] = _new.upper()
        properties.FileProcessor.save_dict_to_json(self.__ALPHABET_JSON_FILE_PATH, settings)
