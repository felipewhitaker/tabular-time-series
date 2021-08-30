import pytest 

from tabular_time_series import __version__
from tabular_time_series.tsgen import TimeSeriesGenerator


def test_version():
    assert __version__ == '0.1.0'

class TestTimeSeriesGenerator:

    @pytest.mark.parametrize(
        'data, order, expected',
        [
            (list(range(10)), 1, [([0], [1]), ([1], [2]), ([2], [3]), ([3], [4]), ([4], [5]), ([5], [6]), ([6], [7]), ([7], [8]), ([8], [9])]),
            (list(range(10)), 2, [([0, 1], [2]), ([1, 2], [3]), ([2, 3], [4]), ([3, 4], [5]), ([4, 5], [6]), ([5, 6], [7]), ([6, 7], [8]), ([7, 8], [9])]),
            (list(range(10)), 3, [([0, 1, 2], [3]), ([1, 2, 3], [4]), ([2, 3, 4], [5]), ([3, 4, 5], [6]), ([4, 5, 6], [7]), ([5, 6, 7], [8]), ([6, 7, 8], [9])])
        ]
    )
    def test_ar(self, data, order, expected):
        tabular = TimeSeriesGenerator(data, order, 1, -1)
        assert list(tabular) == expected

    