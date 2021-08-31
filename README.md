# Tabular Time Series

## Summary

This repo was created as I did not find a function able to transform a time-series (1D) into a tabular format (X, y).

## Usage

### TimeSeriesGenerator

The docstring is as follows. Given a 1D array `data = [0, 1, 2, 3, 4, 5, 6]`, generates `X, y` following the parameters `p`(autoregressive), `s` (seasonal) and `n` (lenght of y).

Therefore, it makes it possible to train a neural network (e.g.) that 2 autoregressive entries (e.g. `p = 2`) and predicts the next two (`n = 2`) using 2 (`n = 2`) entries with lag 4 (`s = 4`).

```python
>> data = [0, 1, 2, 3, 4, 5, 6]
>> p, n = 2, 2
>> ts = TimeSeriesGenerator(data, p, n)
>> for X, y in ts:
...    print(X, y)
    [0, 1] [2, 3]
    [1, 2] [3, 4]
    [2, 3] [4, 5]
    [3, 4] [5, 6]
>> p, n, s = 2, 2, 4
>> ts = TimeSeriesGenerator(data, p, n, s)
>> for X, y in ts:
...    # both y have their respective seasonal entry
...    print(data.index(y[0]) - data.index(X[0]) == s, data.index(y[1]) - data.index(X[1]) == s)
...    print(X, y)
    [0, 1, 2, 3] [4, 5]
    [1, 2, 3, 4] [5, 6]
```

### timeseries2df

Considering that many times a batch array is needed for training, `timeseries2df` can be used to generate a `pandas` DataFrame that will contain columns in the format:

```python
>>> from tabular_time_series.tsdf import timeseries2df
>>> data = list(range(10))
>>> p, n, s = 2, 2, 4
>>> df = timeseries2df(data, p, n, s)
>>> df
   y(ts4)_1  y(ts4)_2  y(t-1)  y(t-0)  y(t+1)  y(t+2)
0         0         1       2       3       4       5
1         1         2       3       4       5       6
2         2         3       4       5       6       7
3         3         4       5       6       7       8
4         4         5       6       7       8       9
```
