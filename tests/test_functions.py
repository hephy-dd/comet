from comet import functions


def assert_linear_range(begin, end, step, ref):
    values = []
    for value in functions.LinearRange(begin, end, step):
        values.append(value)
        if len(values) > len(ref):
            break
    assert values == ref


class TestFunctions:

    def test_linear_range(self):
        assert_linear_range(0, 0, 0, [])
        assert_linear_range(0, 1, 0, [])
        assert_linear_range(1, 0, 0, [])
        assert_linear_range(1, 1, 0, [])

        assert_linear_range(0, 0, 0, [])
        assert_linear_range(0, -1, 0, [])
        assert_linear_range(-1, 0, 0, [])
        assert_linear_range(-1, -1, 0, [])

        assert_linear_range(0, 0, 1, [])
        assert_linear_range(0, 1, 2, [0, 1])
        assert_linear_range(0, 1, 1, [0, 1])
        assert_linear_range(1, 0, 1, [1, 0]) # auto step
        assert_linear_range(1, 1, 1, [])

        assert_linear_range(0, 0, 1, [])
        assert_linear_range(0, -1, 1, [0, -1]) # auto step
        assert_linear_range(-1, 0, 1, [-1, 0])
        assert_linear_range(-1, -1, 1, [])

        assert_linear_range(0, 0, -1, [])
        assert_linear_range(0, 1, -1, [0, 1]) # auto step
        assert_linear_range(1, 0, -1, [1, 0])
        assert_linear_range(1, 1, -1, [])

        assert_linear_range(0, 0, -1, [])
        assert_linear_range(0, -1, -1, [0, -1])
        assert_linear_range(-1, 0, -1, [-1, 0]) # auto step
        assert_linear_range(-1, -1, -1, [])

        assert_linear_range(0, 0, 0, [])
        assert_linear_range(0, 5, 0, [])
        assert_linear_range(5, 0, 0, [])
        assert_linear_range(5, 5, 0, [])

        assert_linear_range(0, 0, 0, [])
        assert_linear_range(0, -5, 0, [])
        assert_linear_range(-5, 0, 0, [])
        assert_linear_range(-5, -5, 0, [])

        assert_linear_range(0, 0, 2.5, [])
        assert_linear_range(0, 5, 2.5, [0, 2.5, 5])
        assert_linear_range(5, 0, 2.5, [5, 2.5, 0])  # auto step
        assert_linear_range(5, 5, 2.5, [])

        assert_linear_range(0, 0, 2.5, [])
        assert_linear_range(0, -5, 2.5, [0, -2.5, -5])  # auto step
        assert_linear_range(-5, 0, 2.5, [-5, -2.5, 0])
        assert_linear_range(-5, -5, 2.5, [])

        assert_linear_range(0, 0, -2.5, [])
        assert_linear_range(0, 5, -2.5, [0, 2.5, 5])  # auto step
        assert_linear_range(5, 0, -2.5, [5, 2.5, 0])
        assert_linear_range(5, 5, -2.5, [])

        assert_linear_range(0, 0, -2.5, [])
        assert_linear_range(0, -5, -2.5, [0, -2.5, -5])
        assert_linear_range(-5, 0, -2.5, [-5, -2.5, 0])  # auto step
        assert_linear_range(-5, -5, -2.5, [])

        assert_linear_range(-2.5, 2.5, -2.5, [-2.5, 0, 2.5])  # auto step
        assert_linear_range(-2.5, 2.5, 2.5, [-2.5, 0, 2.5])
        assert_linear_range(2.5, -2.5, 2.5, [2.5, 0, -2.5])  # auto step
        assert_linear_range(2.5, -2.5, -2.5, [2.5, 0, -2.5])

        assert_linear_range(0, 1.001e-15, 2e-16, [0, 2e-16, 4e-16, 6e-16, 8e-16, 1e-15, 1.001e-15])  # jump
        assert_linear_range(1e-15, 0, -2e-16, [1e-15, 8e-16, 6e-16, 4e-16, 2e-16, 0])  # auto step
        assert_linear_range(0, 1, 0.1, [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

        assert_linear_range(-2.5e-12, 2.5e-12, -2.5e-12, [-2.5e-12, 0, 2.5e-12])  # auto step
        assert_linear_range(-2.5e-12, 2.5e-12, 2.5e-12, [-2.5e-12, 0, 2.5e-12])
        assert_linear_range(2.5e-12, -2.5e-12, 2.5e-12, [2.5e-12, 0, -2.5e-12])  # auto step
        assert_linear_range(2.5e-12, -2.5e-12, -2.5e-12, [2.5e-12, 0, -2.5e-12])

        assert_linear_range(-2.5e+12, 2.5e+12, -2.5e+12, [-2.5e+12, 0, 2.5e+12])  # auto step
        assert_linear_range(-2.5e+12, 2.5e+12, 2.5e+12, [-2.5e+12, 0, 2.5e+12])
        assert_linear_range(2.5e+12, -2.5e+12, 2.5e+12, [2.5e+12, 0, -2.5e+12])  # auto step
        assert_linear_range(2.5e+12, -2.5e+12, -2.5e+12, [2.5e+12, 0, -2.5e+12])

        assert_linear_range(-2.5e-24, 2.5e-24, -2.5e-24, [-2.5e-24, 0, 2.5e-24])  # auto step
        assert_linear_range(-2.5e-24, 2.5e-24, 2.5e-24, [-2.5e-24, 0, 2.5e-24])
        assert_linear_range(2.5e-24, -2.5e-24, 2.5e-24, [2.5e-24, 0, -2.5e-24])  # auto step
        assert_linear_range(2.5e-24, -2.5e-24, -2.5e-24, [2.5e-24, 0, -2.5e-24])

        assert_linear_range(-2.5e+24, 2.5e+24, -2.5e+24, [-2.5e+24, 0, 2.5e+24])  # auto step
        assert_linear_range(-2.5e+24, 2.5e+24, 2.5e+24, [-2.5e+24, 0, 2.5e+24])
        assert_linear_range(2.5e+24, -2.5e+24, 2.5e+24, [2.5e+24, 0, -2.5e+24])  # auto step
        assert_linear_range(2.5e+24, -2.5e+24, -2.5e+24, [2.5e+24, 0, -2.5e+24])

        assert_linear_range(0, 0, 5, [])
        assert_linear_range(0, 1, 5, [0, 1])  # limited step
        assert_linear_range(1, 0, 5, [1, 0])  # limited step
