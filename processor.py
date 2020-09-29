import io
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import sympy as sy

functions_list = []


class PlotWidget:
    def __init__(self):
        self.x = sy.Symbol("x")

    @staticmethod
    def fig2img(fig):
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        return buf

    def function(self, text, x, funs: dict = None) -> Callable:
        # try:
        return eval(
            text,
            funs
            or {
                "x": x,
                "sin": np.sin,
                "cos": np.cos,
                "tg": np.tan,
                "ctg": lambda x: 1 / np.tan(x),
                "e": np.exp,
                "sqrt": np.sqrt,
                "ln": np.log,
                "log": np.log10,
            },
        )
        # except Exception as e:
        #     print(e)
        #     return lambda x: 1

    def plot(self, text) -> io.BytesIO:
        x = np.linspace(-10, 10, 20000)
        y = self.function(text, x)

        # plt.set_facecolor("#DCDCDC")
        plt.axhline(y=0, xmin=-10.25, xmax=10.25, color="#000000")
        plt.axvline(x=0, ymin=-10, ymax=10, color="#000000")
        # plt.set_ylim([-2, 2])
        # plt.set_xlim([-5, 5])

        if isinstance(y, int):
            y = np.array([y] * len(x))

        if text in ("sin(x)", "cos(x)"):
            plt.axhline(y=1, xmin=-10.25, xmax=10.25, color="b", linestyle="--")
            plt.axhline(y=-1, xmin=-10.25, xmax=10.25, color="b", linestyle="--")

        plt.plot(x, y, linestyle="-", color="#008000", label=text)
        plt.legend(loc="upper right")

        data = self.fig2img(plt.gcf())
        plt.clf()

        return data
