def create_properties() -> str:
    from enigma.properties import EnigmaProperties, FileProcessor
    properties_filepath = "EnigmaPropertiesFromDocxExample.JSON"
    if FileProcessor.is_json_file(properties_filepath):
        return properties_filepath

    properties = EnigmaProperties(properties_filepath)

    properties.ALPHABET_SETTINGS.alphabet = "АБВГ"

    properties.ROTORS_SETTINGS.save_new_rotor_wiring(1, "ГАБВ")
    properties.ROTORS_SETTINGS.save_new_rotor_wiring(2, "БАГВ")
    properties.ROTORS_SETTINGS.save_new_rotor_wiring(3, "ВГАБ")

    properties.REFLECTOR_SETTINGS.save_pair(("А", "Г"))
    properties.REFLECTOR_SETTINGS.save_pair(("Б", "В"))

    return properties_filepath


if __name__ == "__main__":
    from enigma import Enigma

    source_text = "ГАВ"
    enigma_properties_filepath = create_properties()

    enigma_sender = Enigma(
        ("Б", "В"), rotors_starts_with=("А", "А", "А"),
        path_to_enigma_settings=enigma_properties_filepath,
    )
    enigma_receiver = enigma_sender.copy()

    encrypted_text = enigma_sender.process_text(source_text)
    print(f"Шифруем: '{source_text}' --> '{encrypted_text}'")

    decrypted_text = enigma_receiver.process_text(encrypted_text)
    print(f"Дешифруем: '{encrypted_text}' --> '{decrypted_text}'")
