from enigma.engine.rotor import Rotor


class RotorProcessor:
    def __init__(self, rotors: list[Rotor]):
        self.__ROTORS = [[rotor, 0] for rotor in rotors]
        self.__ROTORS_QTY_MINUS_ONE = len(self.__ROTORS) - 1
        self.__ALPHABET_QTY = len(rotors[0].alphabet)
        self.__ROTATE_REQUIRED = (False, False)

    @property
    def rotors_list(self) -> list[Rotor]:
        return [rotor for rotor, _ in self.__ROTORS]

    def forward(self, char: str) -> str:
        self.__ROTATE_REQUIRED = (True, self.__ROTATE_REQUIRED[1])
        char = char[0]
        for rotor, _ in self.__ROTORS:
            char = rotor.forward(char)
        self.rotate()
        return char

    def backward(self, char: str) -> str:
        self.__ROTATE_REQUIRED = (self.__ROTATE_REQUIRED[0], True)
        char = char[0]
        for rotor, _ in reversed(self.__ROTORS):
            char = rotor.backward(char)
        self.rotate()
        return char

    def rotate(self):
        if not (self.__ROTATE_REQUIRED[0] and self.__ROTATE_REQUIRED[1]):
            return
        self.__ROTORS[0][0].rotate()
        self.__ROTORS[0][1] += 1
        for i in range(self.__ROTORS_QTY_MINUS_ONE):
            if self.__ROTORS[i][1] % self.__ALPHABET_QTY == 0:
                self.__ROTORS[i][1] = 0
                self.__ROTORS[i+1][0].rotate()
                self.__ROTORS[i+1][1] += 1
            else:
                break
        self.__ROTATE_REQUIRED = (False, False)
