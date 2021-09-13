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
        if len(self) > self._min_len(p, n, s):
            return True
        return False

    def __call__(self, new_data: object):
        self._data.append(new_data)

        if not self._check_len(self.p, self.n, self.s):
            b, (s, ar, y) = False, (None, None, None)

        else:
            b, (s, ar, y) = (
                True,
                TimeSeriesGenerator(self._data, self.p, self.n, self.s).__next__(),
            )
            self._data = self._data[1:]

        return b, (s, ar, y)
