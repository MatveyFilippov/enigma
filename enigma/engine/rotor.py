class Rotor:
    @staticmethod
    def __shift_str_to_left(to_shift: str, str_len: int) -> str:
        result = ""
        for i in range(1, str_len):
            result += to_shift[i]
        result += to_shift[0]
        return result

    def __init__(self, alphabet: str, wiring: str, initial_char: str | None = None):
        self.__WIRING_LEN = len(wiring)
        if not (self.__WIRING_LEN == len(alphabet) == len(set(alphabet)) == len(set(wiring))):
            raise IndexError(
                "Invalid alphabet and wiring for rotor, they should be same len and contains only uniq chars..."
            )

        self.__ALPHABET = alphabet
        self.__wiring = wiring

        if initial_char:
            self.set_position(initial_char)

    @property
    def wiring(self) -> str:
        return self.__wiring

    @property
    def alphabet(self) -> str:
        return self.__ALPHABET

    def set_position(self, initial_char: str):
        initial_char = initial_char[0]
        if initial_char not in self.__wiring:
            raise ValueError("Can't set position to char that not exists in wiring")
        while self.__wiring[0] != initial_char:
            self.rotate()

    def rotate(self):
        self.__wiring = Rotor.__shift_str_to_left(self.__wiring, self.__WIRING_LEN)

    def forward(self, char: str) -> str:
        return self.__wiring[self.__ALPHABET.index(char[0])]

    def backward(self, char: str) -> str:
        return self.__ALPHABET[self.__wiring.index(char[0])]
