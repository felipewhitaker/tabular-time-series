from collections.abc import Iterator
from typing import Sequence, Tuple


class TimeSeriesGenerator(Iterator):
    def __init__(self, data: Sequence, p: int, n: int, s: int = -1) -> None:
        """
        Iterator that receives `time series data` (rows, cols) and can
        be iterated over, returning `X` like ([s + n] + p,) and `y` like
        (n,) such that:

        >> np.where(y == y[0])[0].item() - np.where(X == X[0])[0].item()  == s
        >> np.where(y == y[0])[0].item() - np.where(X == X[-1])[0].item() == 1

        Parameters:
        ----------
        data : np.array of shape (n,)
        p : int
        n : int
        s : int

        Returns:
        -------
        None
        """

        super().__init__()

        assert (
            s > 0 or p > 0
        ) and n > 0, f"Please set (s = {s} > 0 or p = {p} > 0) and {n} > 0"
        assert (
            len(data) > s
        ), f"Sequence lenght len(data) = {len(data)} must be greater than seasonal component s = {s}"
        assert (
            len(data) >= n + p
        ), f"Impossible to generate sequence from given parameters p = {p}, n = {n}, s = {s} for sequence of lenght len(data) = {len(data)}"

        self.S = -1
        if s > 0:
            assert s >= p + n, "`s` and `p` values shouldn't be overlapping"
            self.S = s

        self.data = data

        self.p = p
        self.n = n

        self.s = 0

        self.curr = s - p if s > 0 else 0
        return

    def __len__(self) -> int:
        return len(self.data) - self.n - self.p

    def __getitem__(self, i) -> Tuple[Sequence, Sequence, Sequence]:
        if self.curr > len(self):
            raise IndexError

        ys = self.data[0:0]  # empty
        if self.S > -1:
            ys = self.data[self.s : self.s + self.n]
            self.s += 1

        ar = self.data[i : i + self.p]  # autoregressive
        yt = self.data[i + self.p : i + self.p + self.n]  # y for prediction
        return ys, ar, yt

    def __next__(self) -> Tuple[Sequence, Sequence, Sequence]:
        try:
            s, ar, y = self[self.curr]
        except IndexError:
            raise StopIteration()
        self.curr += 1
        return s, ar, y
