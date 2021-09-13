import pytest

from tabular_time_series import __version__
from tabular_time_series.tsgenerator import TimeSeriesGenerator
from tabular_time_series.tsdf import timeseries2df
from tabular_time_series.tsgeneratoronline import TimeSeriesGeneratorOnline


def test_version():
    assert __version__ == "0.1.0"


test_data_list = list(range(10))


class Test_TimeSeriesGenerator:
    @pytest.mark.parametrize(
        "data, order, yorder, sorder",
        [
            (test_data_list, 0, 0, 0),
            (test_data_list, 10, 1, 0),
            (test_data_list, 1, 10, 0),
            (test_data_list, 0, 1, 10),
        ],
    )
    def test_assertions(self, data, order, yorder, sorder):
        with pytest.raises(AssertionError):
            tabular = TimeSeriesGenerator(data, order, yorder, sorder)

    @pytest.mark.parametrize(
        "data, order, yorder, sorder, expected",
        [
            (test_data_list, 9, 1, 0, [([], [0, 1, 2, 3, 4, 5, 6, 7, 8], [9])]),
        ],
    )
    def test_ar(self, data, order, yorder, sorder, expected):
        tabular = TimeSeriesGenerator(data, order, yorder, sorder)
        assert list(tabular) == expected

    @pytest.mark.parametrize(
        "data, order, yorder, sorder, expected",
        [
            (test_data_list, 1, 9, 0, [([], [0], [1, 2, 3, 4, 5, 6, 7, 8, 9])]),
        ],
    )
    def test_ylen(self, data, order, yorder, sorder, expected):
        tabular = TimeSeriesGenerator(data, order, yorder, sorder)
        assert list(tabular) == expected

    @pytest.mark.parametrize(
        "data, order, yorder, sorder, expected",
        [
            (test_data_list, 0, 1, 9, [([0], [], [9])]),
        ],
    )
    def test_sorder(self, data, order, yorder, sorder, expected):
        tabular = TimeSeriesGenerator(data, order, yorder, sorder)
        assert list(tabular) == expected

    @pytest.mark.parametrize(
        "data, order, ylen, sorder, expected",
        [
            (
                test_data_list,
                1,
                1,
                0,
                [
                    ([], [0], [1]),
                    ([], [1], [2]),
                    ([], [2], [3]),
                    ([], [3], [4]),
                    ([], [4], [5]),
                    ([], [5], [6]),
                    ([], [6], [7]),
                    ([], [7], [8]),
                    ([], [8], [9]),
                ],
            ),
        ],
    )
    def test_basic(self, data, order, ylen, sorder, expected):
        tabular = TimeSeriesGenerator(data, order, ylen, sorder)
        assert list(tabular) == expected


class Test_timeseries2df:
    @pytest.mark.parametrize(
        "data, order, yorder, sorder, expected",
        [
            (
                test_data_list,
                1,
                1,
                2,
                {
                    "y(ts2)_1": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7},
                    "y(t-0)": {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8},
                    "y(t+1)": {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8, 7: 9},
                },
            )
        ],
    )
    def test_function(self, data, order, yorder, sorder, expected):
        df = timeseries2df(data, order, yorder, sorder)
        assert df.to_dict() == expected


class Test_TimeSeriesGeneratorOnline:
    @pytest.mark.parametrize(
        "data, order, yorder, sorder, expected",
        [
            (
                test_data_list,
                1,
                1,
                2,
                [
                    [False, None, None, None],
                    [False, None, None, None],
                    [False, None, None, None],
                    [True, [1], [2], [3]],
                    [True, [2], [3], [4]],
                    [True, [3], [4], [5]],
                    [True, [4], [5], [6]],
                    [True, [5], [6], [7]],
                    [True, [6], [7], [8]],
                    [True, [7], [8], [9]],
                ],
            ),
        ],
    )
    def test_function(self, data, order, yorder, sorder, expected):
        tsgo = TimeSeriesGeneratorOnline(order, yorder, sorder)

        for i, X in enumerate(data):
            b, (s, ar, y) = tsgo(X)
            assert [b, s, ar, y] == expected[i]
