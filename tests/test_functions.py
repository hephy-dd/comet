from comet import functions


def assert_linear_range(begin, end, step, ref):
    l = []
    for value in functions.LinearRange(begin, end, step):
        l.append(value)
        if len(l) > len(ref):
            break
    assert l == ref


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
        assert_linear_range(0, 1, 2, [])
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

        assert_linear_range(0, 1e-5, 2e-6, [0, 2e-6, 4e-6, 6e-6, 8e-6, 1e-5])
        assert_linear_range(1e-5, 0, 2e-6, [1e-5, 8e-6, 6e-6, 4e-6, 2e-6, 0])

        assert_linear_range(0, 1.001e-15, 2e-16, [0, 2e-16, 4e-16, 6e-16, 8e-16, 1e-15, 1.001e-15])  # jump
        assert_linear_range(1e-15, 0, -2e-16, [1e-15, 8e-16, 6e-16, 4e-16, 2e-16, 0])  # auto step

        assert_linear_range(0, 1, .3, [0, .3, .6, .9, 1.])
        assert_linear_range(1, 0, -.3, [1, .7, .4, .1, 0])

        assert_linear_range(0, .7, .2, [0, .2, .4, .6, .7])
        assert_linear_range(.7, 0, -.2, [.7, .5, .3, .1, 0])
