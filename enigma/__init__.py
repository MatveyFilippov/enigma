from enigma import properties
from enigma.engine import swapper
from enigma.rotor_processor import RotorProcessor


class Enigma:
    def __init__(self, *plugboard_pairs: tuple[str, str], rotors_starts_with: tuple[str, ...] | None = None,
                 path_to_enigma_settings: str = "EnigmaProperties.JSON"):
        self.PROPERTIES = properties.EnigmaProperties(path_to_enigma_settings)

        self.ALPHABET = self.PROPERTIES.ALPHABET_SETTINGS.alphabet
        rotors_list = self.PROPERTIES.ROTORS_SETTINGS.rotor_objs_list
        self.ROTOR_PROCESSOR = RotorProcessor(rotors_list)
        self.REFLECTOR = self.PROPERTIES.REFLECTOR_SETTINGS.reflector_obj
        self.PLUGBOARD = swapper.Plugboard(*plugboard_pairs)

        if rotors_starts_with:
            rotors_qty = len(rotors_list)
            if rotors_qty > len(rotors_starts_with):
                raise ValueError("You forget to set rotors start position (invalid qty)")
            for i in range(rotors_qty):
                rotors_list[i].set_position(rotors_starts_with[i])

    def copy(self):
        return Enigma(
            *self.PLUGBOARD.pairs, rotors_starts_with=tuple(
                rotor.wiring[0] for rotor in self.ROTOR_PROCESSOR.rotors_list
            ), path_to_enigma_settings=self.PROPERTIES.enigma_json_file_path,
        )

    def process_text(self, text: str, ignore_unknown_char=False) -> str:
        result = ""
        for char in text:
            result += self.process_char(char, ignore_unknown_char)
        return result

    def process_char(self, char: str, ignore_unknown_char=False) -> str:
        char = char[0].upper()
        if char not in self.ALPHABET and ignore_unknown_char:
            return char

        char = self.PLUGBOARD.swap(char)
        char = self.ROTOR_PROCESSOR.forward(char)
        char = self.REFLECTOR.reflect(char)
        char = self.ROTOR_PROCESSOR.backward(char)
        char = self.PLUGBOARD.swap(char)

        return char
