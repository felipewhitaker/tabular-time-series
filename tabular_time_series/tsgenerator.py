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

        Thus

        >> data = [0, 1, 2, 3, 4, 5, 6]
        >> p, n = 2, 2
        >> ts = TimeSeriesGenerator(data, p, n)
        >> for X, y in ts:
        ...    print(X.shape, y.shape)
        ...    print(X, y)
            [0, 1] [2, 3]
            [1, 2] [3, 4]
            [2, 3] [4, 5]
            [3, 4] [5, 6]
        >> p, n, s = 2, 2, 4
        >> ts = TimeSeriesGenerator(data, p, n, s)
        >> for X, y in ts:
        ...    diff = np.where(data == y[0])[0].item() - np.where(data == X[0])[0].item()
        ...    print(X.shape, y.shape, diff) == (n + p,) (n,) s
        ...    print(X, y)
            [0, 1, 2, 3] [4, 5]
            [1, 2, 3, 4] [5, 6]

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

        # assert n >= 1, "`n` was set to zero: shouldn't some `y` be predicted?"
        # assert (
        #     p >= 0 or s >= 0
        # ), "Neither `p` nor `s` were set: which data will be used to predict `y`?"
        # assert (
        #     len(data) - n - p - (n if s > 0 else 0) >= 0
        # ), "Impossible to generate even one instance"
        # assert (
        #     len(data) - s > 0
        # ), f"Given data of len {len(data)} can not generate seasonal of {s}"

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


if __name__ == "__main__":

    import numpy as np
    from numpy import array, int64

    test_data_list = list(range(10))
    test_data_numpy = np.arange(10)

    order, yorder, sorder = 1, 1, 0
    res = list(TimeSeriesGenerator(test_data_numpy, order, yorder, sorder))
    expected = np.array((array([], dtype=int64), array([0]), array([1])))
    print(np.array(res[0]) == expected)

    # for test_data, name_data in [
    #     (test_data_list, "test_data_list"),
    #     (test_data_numpy, "test_data_numpy"),
    # ]:
    #     for order, yorder, sorder in [
    #         # (len(test_data) - 1, 1, 0),
    #         # (1, len(test_data) - 1, 0),
    #         # (1, len(test_data) - 1, 0),
    #         # (0, 1, len(test_data) - 1),
    #         (1, 1, 0),
    #     ]:

    #         res = list(TimeSeriesGenerator(test_data, order, yorder, sorder))

    #         print(f"({name_data}, {order}, {yorder}, {sorder}, {res}),")
