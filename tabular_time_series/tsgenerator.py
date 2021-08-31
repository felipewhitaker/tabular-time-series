from collections.abc import Iterator
from typing import Union, List, Tuple


class TimeSeriesGenerator(Iterator):
    def __init__(
        self, data: Union[list], p: int, n: int, s: int = -1
    ) -> Tuple[List, List]:
        """
        Iterator that receives `time series data` (rows, cols) and can
        be iterated over, returning `X` like ([s + n] + p,) and `y` like
        (n,) such that:

        >> np.where(y == y[0])[0].item() - np.where(X == X[0])[0].item()  == s
        >> np.where(y == y[0])[0].item() - np.where(X == X[-1])[0].item() == 1

        Thus

        >> data = np.array([0, 1, 2, 3, 4, 5, 6])
        >> p, n = 2, 2
        >> ts = TimeSeries(data, p, n)
        >> for X, y in ts:
        ...    print(X.shape, y.shape)
        ...    print(X, y)
            (2,) (2,)
            [0. 1.] [2 3]
            (2,) (2,)
            [1. 2.] [3 4]
            (2,) (2,)
            [2. 3.] [4 5]
            (2,) (2,)
            [3. 4.] [5 6]
        >> p, n, s = 2, 2, 4
        >> ts = TimeSeries(data, p, n, s)
        >> for X, y in ts:
        ...    diff = np.where(data == y[0])[0].item() - np.where(data == X[0])[0].item()
        ...    print(X.shape, y.shape, diff) == (n + p,) (n,) s
        ...    print(X, y)
            (4,) (2,)
            [0 1 2 3] [4 5]
            (4,) (2,)
            [1 2 3 4] [5 6]

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

        # assert (len(data) - n - s) // p >= 1, "There should be at least one `p` length array to be returned"
        assert n >= 1, "`n` was set to zero: shouldn't some `y` be predicted?"
        assert (
            p >= 0 or s >= 0
        ), "Neither `p` nor `s` were set: which data will be used to predict `y`?"
        assert (
            len(data) - n - p - n * (s if s > 0 else 0) >= 0
        ), "Impossible to generate even one instance"

        self.S = -1
        if s > 0:
            assert s >= p + n, "`s` and `p` values shouldn't be overlapping"
            self.S = s

        self.data = list(data)

        self.p = p
        self.n = n

        self.s = 0

        self.curr = s - p if s > 0 else 0  # s - p if s > p else 0
        return

    def __len__(self):
        return len(self.data) - self.n - self.p

    def __getitem__(self, i):
        if self.curr > len(self):
            raise IndexError

        ys = []
        if self.S > -1:
            ys = self.data[self.s : self.s + self.n]
            self.s += 1

        ar = self.data[i : i + self.p]  # autoregressive
        yt = self.data[i + self.p : i + self.p + self.n]  # y for prediction
        return ys + ar, yt

    def __next__(self):
        try:
            X, y = self[self.curr]
        except IndexError:
            raise StopIteration()
        self.curr += 1
        return X, y
