def create_random_properties(path: str, alphabet: str):
    from enigma.properties import EnigmaProperties
    properties = EnigmaProperties(path)
    properties.ALPHABET_SETTINGS.alphabet = alphabet
    properties.create_random_rotors(rotors_qty=3)
    properties.create_random_reflector()


def get_rotors_settings(path: str) -> tuple[str, ]:
    from enigma.properties.alphabet import AlphabetSettings
    print("Введите начальное положение трёх роторов")
    print("Символы, которые вы можете использовать")
    print(f" * '{AlphabetSettings(path).alphabet}'")
    return tuple(input("Введите три символа: ").replace(" ", ""))


def get_plugboard_settings(path: str) -> tuple[tuple[str, str], ...]:
    from enigma.properties.alphabet import AlphabetSettings
    print("\n\nВведите настройки соединительной панели")
    print("Например, если вы хотите добавить пары 'М-Ф' и 'Ф-М', введите 'МФ' или 'ФМ'")
    print("Символы, которые вы можете использовать")
    print(f" * '{AlphabetSettings(path).alphabet}'")
    pairs = []
    for pair in input("Введите пары через запятую: ").replace(" ", "").split(","):
        try:
            pairs.append((pair[0], pair[1]))
        except IndexError:
            continue
    return tuple(pairs)


if __name__ == "__main__":
    import sys
    from enigma.properties import FileProcessor
    from enigma import Enigma

    PATH_TO_JSON_ENIGMA_PROPERTIES = "EnigmaPropertiesRUS.JSON"
    if not FileProcessor.is_json_file(PATH_TO_JSON_ENIGMA_PROPERTIES):
        print("Файл с настройками не существует, могу я создать его рандомно?")
        decision = input("'NO' чтоб прервать процесс, любой символ чтоб продолжить: ")
        if decision.strip() == "NO":
            sys.exit(0)
        create_random_properties(
            path=PATH_TO_JSON_ENIGMA_PROPERTIES, alphabet="АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ123456789"
        )
        print("\n")

    rotors_settings = get_rotors_settings(PATH_TO_JSON_ENIGMA_PROPERTIES)
    plugboard_settings = get_plugboard_settings(PATH_TO_JSON_ENIGMA_PROPERTIES)

    ENIGMA = Enigma(
        *plugboard_settings, rotors_starts_with=rotors_settings, path_to_enigma_settings=PATH_TO_JSON_ENIGMA_PROPERTIES,
    )

    print("\n\n * Введите текст для шифровки (поддерживается любой символ)")
    text = ENIGMA.process_text(text=input(": "), ignore_unknown_char=True)
    print("\n * Ваш текст, пропущенный через Энигму", f": {text}", sep="\n")
