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

import math

from trade.function import MacdHistogram
from trade.indicator import Indicator, Signal

class MacdSignalCrossoverIndicator(Indicator):
    def __init__(self, input_, short_period, long_period, signal_period):
        self.input = input_
        self.__short_period = short_period
        self.__long_period = long_period
        self.__signal_period = signal_period

        self.__macd_histogram = MacdHistogram(self.input, self.__short_period, self.__long_period, self.__signal_period)

        Indicator.__init__(self)

    def _next(self):
        self.__macd_histogram._exhaust_input()

        if len(self.__macd_histogram) < 2 or len(self) == len(self.__macd_histogram) - 1:
            raise StopIteration

        last_hist = self.__macd_histogram[len(self)]
        this_hist = self.__macd_histogram[len(self) + 1]

        if math.copysign(1, last_hist) != math.copysign(1, this_hist):
            self._values.append(Signal.BUY if math.copysign(1, this_hist) > 0 else Signal.SELL)
        else:
            self._values.append(Signal.HOLD)
