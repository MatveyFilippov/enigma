import random
import string
import unittest
from enigma import Enigma
from enigma.properties import EnigmaProperties, FileProcessor
import os


PROPERTIES_FILEPATH = "EnigmaTestPropertiesRUS.JSON"
ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ123456789"


class MyTestCase(unittest.TestCase):
    def delete_properties_if_exists(self):
        if FileProcessor.is_json_file(PROPERTIES_FILEPATH):
            os.remove(PROPERTIES_FILEPATH)
        self.assertFalse(FileProcessor.is_json_file(PROPERTIES_FILEPATH))

    def check_creating_properties(self):
        properties = EnigmaProperties(PROPERTIES_FILEPATH)

        properties.ALPHABET_SETTINGS.alphabet = ALPHABET
        self.assertSetEqual(set(ALPHABET), set(properties.ALPHABET_SETTINGS.alphabet))

        properties.create_random_rotors(rotors_qty=3)
        self.assertEqual(3, len(properties.ROTORS_SETTINGS.rotor_objs_list))

        properties.create_random_reflector()
        self.assertEqual(len(ALPHABET)/2, len(properties.REFLECTOR_SETTINGS.pairs))

    def test_overflow_properties(self):
        self.delete_properties_if_exists()
        self.check_creating_properties()
        try:
            self.check_creating_properties()
            self.assertTrue(False, msg="Не удалось перегрузить")
        except Exception:
            pass
        os.remove(PROPERTIES_FILEPATH)
        self.assertFalse(FileProcessor.is_json_file(PROPERTIES_FILEPATH))

    def get_new_enigma(self) -> Enigma:
        self.delete_properties_if_exists()
        self.check_creating_properties()

        rotors_settings = tuple(random.choice(ALPHABET) for _ in range(3))
        plugboard_settings = []
        temp_alphabet = list(ALPHABET)
        random.shuffle(temp_alphabet)
        for _ in range(random.randint(1, int(len(ALPHABET)/2))):
            plugboard_settings.append((temp_alphabet.pop(), temp_alphabet.pop()))
        plugboard_settings = tuple(plugboard_settings)

        return Enigma(
            *plugboard_settings, rotors_starts_with=rotors_settings,
            path_to_enigma_settings=PROPERTIES_FILEPATH,
        )

    def test_crypto(self):
        e = self.get_new_enigma()
        for _ in range(1000):
            to_ = "".join([random.choice(ALPHABET) for _ in range(random.randint(1, len(ALPHABET)))])
            from_ = e.process_text(to_)
            self.assertNotEqual(to_, from_)
            self.assertEqual(len(to_), len(from_))

    def test_decrypto_by_copied_enigma(self):
        e1 = self.get_new_enigma()
        e2 = e1.copy()
        for _ in range(1000):
            to_ = "".join([random.choice(ALPHABET) for _ in range(random.randint(1, len(ALPHABET)))])
            from_ = e1.process_text(to_)
            self.assertNotEqual(to_, from_)
            self.assertEqual(to_, e2.process_text(from_))

    def test_unknown_char(self):
        e = self.get_new_enigma()
        eng_char = random.choice(string.ascii_uppercase)
        self.assertNotIn(eng_char, ALPHABET)
        try:
            e.process_char(eng_char)
            self.assertTrue(False, msg="Process invalid char")
        except ValueError as ex:
            self.assertEqual("substring not found", str(ex))
        self.assertEqual(eng_char, e.process_char(eng_char, ignore_unknown_char=True))


if __name__ == '__main__':
    unittest.main()
