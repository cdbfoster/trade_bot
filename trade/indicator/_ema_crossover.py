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

from trade.function import Macd
from trade.indicator import Indicator, Signal

class EmaCrossover(Indicator):
    def __init__(self, input_, short_period, long_period):
        self.input = input_
        self.__short_period = short_period
        self.__long_period = long_period

        self.__macd = Macd(self.input, self.__short_period, self.__long_period)

        Indicator.__init__(self)

    def _next(self):
        self.__macd._exhaust_input()

        if len(self.__macd) < 2 or len(self) == len(self.__macd) - 1:
            raise StopIteration

        last_macd = self.__macd[len(self)]
        this_macd = self.__macd[len(self) + 1]

        if math.copysign(1, last_macd) != math.copysign(1, this_macd):
            self._values.append(Signal.BUY if math.copysign(1, this_macd) > 0 else Signal.SELL)
        else:
            self._values.append(Signal.HOLD)
