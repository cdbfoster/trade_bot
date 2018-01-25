# This file is part of trade_bot.
#
# trade_bot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# trade_bot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with trade_bot.  If not, see <http://www.gnu.org/licenses/>.

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

from trade.indicator import Indicator, Signal

class Grapher:
    class _Plot:
        colors = ['', 'b', 'g', 'r', 'c', 'm', 'y']

        def __init__(self, time, ranges):
            self.time = time
            self.major_interval = None
            self.minor_count = None
            self.ranges = ranges

        def show(self, major_interval=None, minor_count=None):
            plt.xlim(xmin=self.time[0], xmax=self.time[-1])

            if self.major_interval is not None:
                plt.gca().xaxis.set_major_locator(MultipleLocator(self.major_interval))
            elif major_interval is not None:
                plt.gca().xaxis.set_major_locator(MultipleLocator(major_interval))
            plt.grid(b=True, which='major', linewidth=1.0)

            if self.minor_count is not None:
                plt.gca().xaxis.set_minor_locator(MultipleLocator(self.minor_count))
            elif minor_count is not None:
                plt.gca().xaxis.set_minor_locator(MultipleLocator(minor_count))
            plt.grid(b=True, which='minor', linewidth=0.3)
            plt.minorticks_on()

            for i, range_ in enumerate(self.ranges):
                if not isinstance(range_, Indicator):
                    plt.plot(self.time[len(self.time) - len(range_):], range_, Grapher._Plot.colors[i % len(Grapher._Plot.colors)] + '-')
                elif not isinstance(self.ranges[0], Indicator):
                    buy_time = [self.time[len(self.time) - len(range_) + i] for i, signal in enumerate(range_) if signal is Signal.BUY]
                    buy_price = [self.ranges[0][len(self.ranges[0]) - len(range_) + i] for i, signal in enumerate(range_) if signal is Signal.BUY]
                    plt.plot(buy_time, buy_price, "g^")

                    sell_time = [self.time[len(self.time) - len(range_) + i] for i, signal in enumerate(range_) if signal is Signal.SELL]
                    sell_price = [self.ranges[0][len(self.ranges[0]) - len(range_) + i] for i, signal in enumerate(range_) if signal is Signal.SELL]
                    plt.plot(sell_time, sell_price, "rv")


    def __init__(self, *args, major_interval=None, minor_count=None):
        current_time = args[0][:]
        plots = []
        for arg in args[1:]:
            if isinstance(arg, float) or isinstance(arg, int):
                if plots[-1].major_interval is None:
                    plots[-1].major_interval = arg
                elif plots[-1].minor_count is None:
                    plots[-1].minor_count = arg
            elif len(arg) == 0:
                continue
            elif isinstance(arg[0], float) or isinstance(arg[0], int):
                # This is a new timeline
                current_time = arg[:]
            else:
                plots.append(Grapher._Plot(current_time, [range_[:] if not isinstance(range_, Indicator) else range_ for range_ in arg]))

        for i, plot in enumerate(plots):
            if len(plots) > 1:
                plt.subplot(len(plots), 1, i + 1)

            plot.show(major_interval, minor_count)

        plt.show()
