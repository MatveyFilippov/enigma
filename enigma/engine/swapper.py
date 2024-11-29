import abc


class __PairSwapper(abc.ABC):
    def __init__(self, *pairs: tuple[str, str]):
        self._pairs = {}
        for pair in pairs:
            x, y = pair
            x, y = x[0], y[0]
            if x in self._pairs or y in self._pairs:
                raise KeyError("Char already used in pair, it can be used only once...")
            self._pairs[x] = y
            self._pairs[y] = x

    @property
    def pairs(self) -> tuple[tuple[str, str]]:
        result = []
        used = set()
        for x, y in self._pairs.items():
            if x in used or y in used:
                continue
            result.append((x, y))
            used.add(x)
            used.add(y)
        return tuple(result)

    def _swap(self, char: str) -> str:
        char = char[0]
        if char in self._pairs:
            return self._pairs[char]
        return char

    def __call__(self, char: str) -> str:
        return self._swap(char)


class Plugboard(__PairSwapper):
    def swap(self, char: str) -> str:
        return self._swap(char)


class Reflector(__PairSwapper):
    def __init__(self, *pairs: tuple[str, str], alphabet: str):
        super().__init__(*pairs)
        alphabet = set(alphabet)
        used_chars = set(self._pairs.keys())
        unused_chars = alphabet.difference(used_chars) if len(alphabet) > len(self._pairs) else used_chars.difference(alphabet)
        if len(unused_chars) > 0:
            raise ValueError(f"Differences between pairs and alphabet in: {unused_chars}")

    def reflect(self, char: str) -> str:
        return self._swap(char)
