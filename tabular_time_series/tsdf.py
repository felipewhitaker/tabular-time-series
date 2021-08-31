from .tsgenerator import TimeSeriesGenerator
import pandas as pd  # type: ignore
from typing import Union
import numpy as np


def timeseries2df(
    data: Union[np.array], p: int, n: int, s: int = -1
) -> pd.DataFrame:  # , category_seasonal, test_split = .33):
    """Interface for `TimeSeriesGenerator`, transforming the generator into a `pd.DataFrame`

    Returns:
        p int: autoregressive parameter
        n int: lenght of `y`
        s int: seasonal parameter
    """

    # Define ts
    ts = TimeSeriesGenerator(data, p, n, s)

    # Iterate over
    features, target = [], []
    for i, (X, y) in enumerate(ts):
        features.append(X)
        target.append(y)

    # Set columns
    s_cols = [f"y(ts{s})_{i}" for i in range(1, n + 1)] if s > 0 else []
    x_cols = s_cols + [f"y(t-{i})" for i in range(p)][::-1]
    y_cols = [f"y(t+{i})" for i in range(1, n + 1)]

    # Create DataFrame
    dftime = pd.concat(
        [pd.DataFrame(features, columns=x_cols), pd.DataFrame(target, columns=y_cols)],
        axis=1,
    )

    return dftime
