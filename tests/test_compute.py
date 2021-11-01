import numpy as np
import numpy.testing as nt
import pytest
from dataeng import compute_quantile

DIST1 = [2.7000000000000002, 20.399999999999999, 2.1000000000000001, 1.3, 1.7, 1.7, 1, 9.1999999999999993, 2.6000000000000001, 1.3999999999999999, 3.2000000000000002, 7.7999999999999998, 1.1000000000000001, 3.2999999999999998, 5.2999999999999998, 6.2000000000000002, 15.6,  0.90000000000000002, 1.3999999999999999]
DIST2 = [1.20, 1.20, .60, .80, .00, .03, .00, .00, .00, .70, 2.40, .80, 3.30, 1.07, 7.76, 1.60, .50, 1.70, 8.45, .00]
P90_DIST1 = 10.48
P90_DIST2 = 3.746
P95_DIST1 = 16.08
P95_DIST2 = 7.7945


def test_compute_90_percentile_on_simple_data():
    assert pytest.approx(P90_DIST1, 0.01) == compute_quantile(DIST1)
    assert pytest.approx(P90_DIST2, 0.01) == compute_quantile(DIST2)


def test_compute_95_percentile_on_simple_data():
    assert pytest.approx(P95_DIST1, 0.01) == compute_quantile(DIST1, 0.95)
    assert pytest.approx(P95_DIST2, 0.01) == compute_quantile(DIST2, 0.95)