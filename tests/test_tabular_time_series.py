import pytest 

from tabular_time_series import __version__
from tabular_time_series.tsgenerator import TimeSeriesGenerator
from tabular_time_series.tsdf import timeseries2df


def test_version():
    assert __version__ == '0.1.0'

DATA = list(range(10))

class TestTimeSeriesGenerator:

    def test_invalid_ar(self):
        with pytest.raises(AssertionError):
            tabular = TimeSeriesGenerator(DATA, len(DATA), 1, -1)

    def test_invalid_ylen(self):
        with pytest.raises(AssertionError):
            tabular = TimeSeriesGenerator(DATA, 1, len(DATA), -1)

    def test_invalid_seasonal(self):
        with pytest.raises(AssertionError):
            tabular = TimeSeriesGenerator(DATA, 1, 1, len(DATA))

    def test_invalid_combination(self):
        with pytest.raises(AssertionError):
            p, n = len(DATA), 1
            tabular = TimeSeriesGenerator(DATA, p, n, -1)

    @pytest.mark.parametrize(
        'data, order, expected',
        [
            (DATA, 1, [([0], [1]), ([1], [2]), ([2], [3]), ([3], [4]), ([4], [5]), ([5], [6]), ([6], [7]), ([7], [8]), ([8], [9])]),
            (DATA, 2, [([0, 1], [2]), ([1, 2], [3]), ([2, 3], [4]), ([3, 4], [5]), ([4, 5], [6]), ([5, 6], [7]), ([6, 7], [8]), ([7, 8], [9])]),
            (DATA, 3, [([0, 1, 2], [3]), ([1, 2, 3], [4]), ([2, 3, 4], [5]), ([3, 4, 5], [6]), ([4, 5, 6], [7]), ([5, 6, 7], [8]), ([6, 7, 8], [9])]),
            (DATA, 4, [([0, 1, 2, 3], [4]), ([1, 2, 3, 4], [5]), ([2, 3, 4, 5], [6]), ([3, 4, 5, 6], [7]), ([4, 5, 6, 7], [8]), ([5, 6, 7, 8], [9])]),
            (DATA, 5, [([0, 1, 2, 3, 4], [5]), ([1, 2, 3, 4, 5], [6]), ([2, 3, 4, 5, 6], [7]), ([3, 4, 5, 6, 7], [8]), ([4, 5, 6, 7, 8], [9])]),
            (DATA, 6, [([0, 1, 2, 3, 4, 5], [6]), ([1, 2, 3, 4, 5, 6], [7]), ([2, 3, 4, 5, 6, 7], [8]), ([3, 4, 5, 6, 7, 8], [9])]),
            (DATA, 7, [([0, 1, 2, 3, 4, 5, 6], [7]), ([1, 2, 3, 4, 5, 6, 7], [8]), ([2, 3, 4, 5, 6, 7, 8], [9])]),
            (DATA, 8, [([0, 1, 2, 3, 4, 5, 6, 7], [8]), ([1, 2, 3, 4, 5, 6, 7, 8], [9])]),
            (DATA, 9, [([0, 1, 2, 3, 4, 5, 6, 7, 8], [9])]),
        ]
    )
    def test_ar(self, data, order, expected):
        tabular = TimeSeriesGenerator(data, order, 1, -1)
        assert list(tabular) == expected

    @pytest.mark.parametrize(
        'data, ylen, expected',
        [
            (DATA, 1, [([0], [1]), ([1], [2]), ([2], [3]), ([3], [4]), ([4], [5]), ([5], [6]), ([6], [7]), ([7], [8]), ([8], [9])]),
            (DATA, 2, [([0], [1, 2]), ([1], [2, 3]), ([2], [3, 4]), ([3], [4, 5]), ([4], [5, 6]), ([5], [6, 7]), ([6], [7, 8]), ([7], [8, 9])]),
            (DATA, 3, [([0], [1, 2, 3]), ([1], [2, 3, 4]), ([2], [3, 4, 5]), ([3], [4, 5, 6]), ([4], [5, 6, 7]), ([5], [6, 7, 8]), ([6], [7, 8, 9])]),
            (DATA, 4, [([0], [1, 2, 3, 4]), ([1], [2, 3, 4, 5]), ([2], [3, 4, 5, 6]), ([3], [4, 5, 6, 7]), ([4], [5, 6, 7, 8]), ([5], [6, 7, 8, 9])]),
            (DATA, 5, [([0], [1, 2, 3, 4, 5]), ([1], [2, 3, 4, 5, 6]), ([2], [3, 4, 5, 6, 7]), ([3], [4, 5, 6, 7, 8]), ([4], [5, 6, 7, 8, 9])]),
            (DATA, 6, [([0], [1, 2, 3, 4, 5, 6]), ([1], [2, 3, 4, 5, 6, 7]), ([2], [3, 4, 5, 6, 7, 8]), ([3], [4, 5, 6, 7, 8, 9])]),
            (DATA, 7, [([0], [1, 2, 3, 4, 5, 6, 7]), ([1], [2, 3, 4, 5, 6, 7, 8]), ([2], [3, 4, 5, 6, 7, 8, 9])]),
            (DATA, 8, [([0], [1, 2, 3, 4, 5, 6, 7, 8]), ([1], [2, 3, 4, 5, 6, 7, 8, 9])]),
            (DATA, 9, [([0], [1, 2, 3, 4, 5, 6, 7, 8, 9])]),
        ]
    )
    def test_ylen(self, data, ylen, expected):
        tabular = TimeSeriesGenerator(data, 1, ylen, -1)
        assert list(tabular) == expected

    @pytest.mark.parametrize(
        'data, sorder, expected',
        [
            (DATA, 2, [([0, 1], [2]), ([1, 2], [3]), ([2, 3], [4]), ([3, 4], [5]), ([4, 5], [6]), ([5, 6], [7]), ([6, 7], [8]), ([7, 8], [9])]),
            (DATA, 3, [([0, 2], [3]), ([1, 3], [4]), ([2, 4], [5]), ([3, 5], [6]), ([4, 6], [7]), ([5, 7], [8]), ([6, 8], [9])]),
            (DATA, 4, [([0, 3], [4]), ([1, 4], [5]), ([2, 5], [6]), ([3, 6], [7]), ([4, 7], [8]), ([5, 8], [9])]),
            (DATA, 5, [([0, 4], [5]), ([1, 5], [6]), ([2, 6], [7]), ([3, 7], [8]), ([4, 8], [9])]),
            (DATA, 6, [([0, 5], [6]), ([1, 6], [7]), ([2, 7], [8]), ([3, 8], [9])]),
            (DATA, 7, [([0, 6], [7]), ([1, 7], [8]), ([2, 8], [9])]),
            (DATA, 8, [([0, 7], [8]), ([1, 8], [9])]),
        ]
    )
    def test_sorder(self, data, sorder, expected):
        tabular = TimeSeriesGenerator(data, 1, 1, sorder)
        assert list(tabular) == expected

    @pytest.mark.parametrize(
        'data, order, ylen, sorder, expected',
        [
            (DATA, 1, 1, 2, [([0, 1], [2]), ([1, 2], [3]), ([2, 3], [4]), ([3, 4], [5]), ([4, 5], [6]), ([5, 6], [7]), ([6, 7], [8]), ([7, 8], [9])]),
            (DATA, 1, 1, 3, [([0, 2], [3]), ([1, 3], [4]), ([2, 4], [5]), ([3, 5], [6]), ([4, 6], [7]), ([5, 7], [8]), ([6, 8], [9])]),
            (DATA, 1, 1, 4, [([0, 3], [4]), ([1, 4], [5]), ([2, 5], [6]), ([3, 6], [7]), ([4, 7], [8]), ([5, 8], [9])]),
            (DATA, 1, 1, 5, [([0, 4], [5]), ([1, 5], [6]), ([2, 6], [7]), ([3, 7], [8]), ([4, 8], [9])]),
            (DATA, 1, 1, 6, [([0, 5], [6]), ([1, 6], [7]), ([2, 7], [8]), ([3, 8], [9])]),
            (DATA, 1, 1, 7, [([0, 6], [7]), ([1, 7], [8]), ([2, 8], [9])]),
            (DATA, 1, 1, 8, [([0, 7], [8]), ([1, 8], [9])]),
            (DATA, 1, 2, 3, [([0, 1, 2], [3, 4]), ([1, 2, 3], [4, 5]), ([2, 3, 4], [5, 6]), ([3, 4, 5], [6, 7]), ([4, 5, 6], [7, 8]), ([5, 6, 7], [8, 9])]),
            (DATA, 2, 1, 3, [([0, 1, 2], [3]), ([1, 2, 3], [4]), ([2, 3, 4], [5]), ([3, 4, 5], [6]), ([4, 5, 6], [7]), ([5, 6, 7], [8]), ([6, 7, 8], [9])]),
            (DATA, 2, 1, 4, [([0, 2, 3], [4]), ([1, 3, 4], [5]), ([2, 4, 5], [6]), ([3, 5, 6], [7]), ([4, 6, 7], [8]), ([5, 7, 8], [9])]),
            (DATA, 2, 1, 5, [([0, 3, 4], [5]), ([1, 4, 5], [6]), ([2, 5, 6], [7]), ([3, 6, 7], [8]), ([4, 7, 8], [9])]),
            (DATA, 2, 1, 6, [([0, 4, 5], [6]), ([1, 5, 6], [7]), ([2, 6, 7], [8]), ([3, 7, 8], [9])]),
            (DATA, 2, 1, 7, [([0, 5, 6], [7]), ([1, 6, 7], [8]), ([2, 7, 8], [9])]),
            (DATA, 3, 1, 4, [([0, 1, 2, 3], [4]), ([1, 2, 3, 4], [5]), ([2, 3, 4, 5], [6]), ([3, 4, 5, 6], [7]), ([4, 5, 6, 7], [8]), ([5, 6, 7, 8], [9])]),
            (DATA, 3, 1, 5, [([0, 2, 3, 4], [5]), ([1, 3, 4, 5], [6]), ([2, 4, 5, 6], [7]), ([3, 5, 6, 7], [8]), ([4, 6, 7, 8], [9])]),
            (DATA, 3, 1, 6, [([0, 3, 4, 5], [6]), ([1, 4, 5, 6], [7]), ([2, 5, 6, 7], [8]), ([3, 6, 7, 8], [9])]),
            (DATA, 4, 1, 5, [([0, 1, 2, 3, 4], [5]), ([1, 2, 3, 4, 5], [6]), ([2, 3, 4, 5, 6], [7]), ([3, 4, 5, 6, 7], [8]), ([4, 5, 6, 7, 8], [9])]),
        ]
    )
    def test_parameters_mix(self, data, order, ylen, sorder, expected):
        tabular = TimeSeriesGenerator(data, order, ylen, sorder)
        assert list(tabular) == expected

class TestGetDF:

    @pytest.mark.parametrize(
        'data, order, yorder, sorder, expected',
        [
            (DATA, 1, 1, 2, {'y(ts2)_1': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}, 'y(t-0)': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}, 'y(t+1)': {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8, 7: 9}})
        ]
    )
    def test_function(self, data, order, yorder, sorder, expected):
        df = timeseries2df(data, order, yorder, sorder)
        assert df.to_dict() == expected