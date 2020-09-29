from unittest import TestCase

import numpy as np

from processor import PlotWidget


class TestPlotter(TestCase):
    def test_image(self):
        data = PlotWidget().plot("cos(x)")

        with open("tests/fixtures/image.png", "rb") as f:
            self.assertEqual(f.read(), data.read())

    def test_function(self):
        pw = PlotWidget()
        x = np.linspace(-10, 10, 10)

        y = pw.function("cos(x)", x)
        self.assertEqual(
            list(y),
            [
                -0.8390715290764524,
                0.07613012462407193,
                0.7467529543114478,
                -0.9816740047110791,
                0.4436660217022289,
                0.4436660217022289,
                -0.9816740047110789,
                0.746752954311449,
                0.07613012462407105,
                -0.8390715290764524,
            ],
        )

        y = pw.function("tg(x)", x)
        self.assertEqual(
            list(y),
            [
                -0.6483608274590866,
                -13.097284364993643,
                0.8906580297256232,
                -0.1941255059835998,
                -2.0199703317182243,
                2.0199703317182243,
                0.1941255059836007,
                -0.89065802972562,
                13.097284364993795,
                0.6483608274590866,
            ],
        )
