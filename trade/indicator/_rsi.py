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

from trade.function import Rsi as RsiFunction
from trade.indicator import Indicator, Signal

class Rsi(Indicator):
    def __init__(self, input_, period, threshold):
        self.input = input_
        self.__period = period
        self.__threshold = threshold

        self.__rsi = RsiFunction(self.input, self.__period)

        Indicator.__init__(self)

    def _next(self):
        self.__rsi._exhaust_input()

        if len(self.__rsi) == 0 or len(self) == len(self.__rsi):
            raise StopIteration

        if self.__rsi[len(self)] > 100 - self.__threshold:
            self._values.append(Signal.SELL)
        elif self.__rsi[len(self)] < self.__threshold:
            self._values.append(Signal.BUY)
        else:
            self._values.append(Signal.HOLD)
