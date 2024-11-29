from enigma import properties
from enigma.engine.rotor import Rotor
from enigma.properties.alphabet import AlphabetSettings


class RotorsSettings:
    __ROTOR_NAME_STARTS_WITH = "ROTOR_"

    def __init__(self, rotors_json_file_path: str = "RotorsProperties.JSON"):
        properties.FileProcessor.create_file_if_not_exists(rotors_json_file_path, check_json=True)
        self.__ROTORS_JSON_FILE_PATH = rotors_json_file_path

    def __clean_dict_save_only_rotors(self, to_clean: dict[str, str]):
        for key in list(to_clean):
            if not key.startswith(self.__ROTOR_NAME_STARTS_WITH):
                del to_clean[key]

    def save_new_rotor_wiring(self, rotor_id: int, wiring: str):
        settings = properties.FileProcessor.get_dict_from_json(self.__ROTORS_JSON_FILE_PATH)
        settings[f"{self.__ROTOR_NAME_STARTS_WITH}{rotor_id}"] = wiring
        properties.FileProcessor.save_dict_to_json(self.__ROTORS_JSON_FILE_PATH, settings)

    def get_rotor_wiring(self, rotor_id: int) -> str:
        rotor_name = f"{self.__ROTOR_NAME_STARTS_WITH}{rotor_id}"
        settings = properties.FileProcessor.get_dict_from_json(self.__ROTORS_JSON_FILE_PATH)
        if rotor_name not in settings:
            raise KeyError(f"{rotor_name} not set yet...")
        return settings[rotor_name]

    def delete_rotor(self, rotor_id: int):
        rotor_name = f"{self.__ROTOR_NAME_STARTS_WITH}{rotor_id}"
        settings = properties.FileProcessor.get_dict_from_json(self.__ROTORS_JSON_FILE_PATH)
        try:
            del settings[rotor_name]
            properties.FileProcessor.save_dict_to_json(self.__ROTORS_JSON_FILE_PATH, settings)
        except KeyError:
            pass

    @property
    def rotor_ids(self) -> list[str]:
        settings = properties.FileProcessor.get_dict_from_json(self.__ROTORS_JSON_FILE_PATH)
        self.__clean_dict_save_only_rotors(settings)
        ids = [k.removeprefix(self.__ROTOR_NAME_STARTS_WITH) for k in settings]
        return sorted(ids)

    @property
    def rotor_objs_list(self) -> list[Rotor]:
        alphabet_const = AlphabetSettings(self.__ROTORS_JSON_FILE_PATH).alphabet

        settings = properties.FileProcessor.get_dict_from_json(self.__ROTORS_JSON_FILE_PATH)
        self.__clean_dict_save_only_rotors(settings)

        result_dict = {}
        for rotor_name, wiring in settings.items():
            rotor_id = rotor_name.removeprefix(self.__ROTOR_NAME_STARTS_WITH)
            result_dict[rotor_id] = Rotor(alphabet=alphabet_const, wiring=wiring)

        return [result_dict[rotor_id] for rotor_id in self.rotor_ids]
