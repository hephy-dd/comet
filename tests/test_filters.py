from comet.filters import std_mean_filter


def test_std_mean_filter():
    assert std_mean_filter([0.250, 0.249], 0.005) == True
    assert std_mean_filter([0.250, 0.249], 0.0005) == False
