# Tabular Time Series

## Summary

This repo was created as I did not find a function able to transform a time-series (1D) into a tabular format (X, y).

## Usage

### TimeSeriesGenerator

The docstring is as follows. Given a 1D array `data = [0, 1, 2, 3, 4, 5, 6]`, generates `X, y` following the parameters `p`(autoregressive), `s` (seasonal) and `n` (lenght of y).

Therefore, it makes it possible to train a neural network (e.g.) that 2 autoregressive entries (e.g. `p = 2`) and predicts the next two (`n = 2`) using 2 (`n = 2`) entries with lag 4 (`s = 4`).

```python
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
```

### get_df

Considering that many times a batch array is needed for training, `get_df` can be used to generate a `pandas` DataFrame that will contain columns in the format:

- `y(t - 0)`, ..., `y(t - p)` autogressive entries
- `y(t + 0)`, ..., `y(t + n)` predict entries
- `y(ts{s}_0})`, ..., `y(ts{s}_n})` seasonal entries
