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

import numpy as np

from trade.function import Function, FunctionInput, Slope

class Rsi(Function):
    def __init__(self, input_, period):
        self.__input = FunctionInput(input_)
        self.__period = FunctionInput(period)

        self.__slope = FunctionInput(Slope(input_))
        self.__average_gain = None
        self.__average_loss = None

        Function.__init__(self)

    def _first(self):
        self.inputs.update()

        if len(self.__period) == 0 or int(self.__period.max) > len(self.__slope):
            raise StopIteration

        self.inputs.sync({self.__slope: int(self.__period.max)})

        self.__input.consume()
        period = int(min(self.__period.consume(), self.__period.max))
        self.__slope.consume()

        self.__average_gain = np.mean([max(d, 0) for d in self.__slope[self.__slope.consumed - period:self.__slope.consumed]])
        self.__average_loss = np.mean([min(d, 0) for d in self.__slope[self.__slope.consumed - period:self.__slope.consumed]])

        self._values.append(100 - 100 / (1 + self.__average_gain / -self.__average_loss)) # XXX We'll need some kind of zero division protection

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.__period) or len(self) + int(self.__period.max) > len(self.__slope):
            raise StopIteration

        self.__input.consume()
        period = int(min(self.__period.consume(), self.__period.max))
        slope = self.__slope.consume()

        self.__average_gain = (self.__average_gain * (period - 1) + max(slope, 0)) / period
        self.__average_loss = (self.__average_loss * (period - 1) + min(slope, 0)) / period

        self._values.append(100 - 100 / (1 + self.__average_gain / -self.__average_loss))
