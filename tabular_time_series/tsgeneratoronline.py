from .tsgenerator import TimeSeriesGenerator


class TimeSeriesGeneratorOnline:
    def __init__(self, p: int, n: int, s: int = -1) -> None:
        self.p = p
        self.n = n
        self.s = s

        self._data = []
        return

    @staticmethod
    def _min_len(p: int, n: int, s: int):
        return max(p, s) + n

    def __len__(self):
        return len(self._data)

    def _check_len(self, p: int, n: int, s: int):
        if len(self) >= self._min_len(p, n, s):
            return True
        return False

    def __call__(self, new_data: object):
        if not self._check_len(self.p, self.n, self.s):
            if len(self) == 0:
                self._data = [new_data]
            else:
                self._data.append(new_data)

            return False, (None, None, None)

        self._data[: len(self) - 1] = self._data[1:]
        self._data[-1] = new_data

        return True, TimeSeriesGenerator(self._data, self.p, self.n, self.s).__next__()


if __name__ == "__main__":

    from random import randint

    data = [_ for _ in range(10)]

    tsgo = TimeSeriesGeneratorOnline(1, 1, 2)

    print("[")
    for X in data:
        b, (s, ar, y) = tsgo(X)
        print(f"\t[{b}, {s}, {ar}, {y}]", end=",\n")
    print("]")
