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

from trade.function import Function, Difference

class Rsi(Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.__difference = Difference(input_)
        self.__average_gain = None
        self.__average_loss = None

        Function.__init__(self)

    def _first(self):
        self.__difference._update()

        if len(self.__difference) < 2 * self.__period:
            raise StopIteration

        self.__average_gain = np.mean([max(d, 0) for d in self.__difference[:self.__period]])
        self.__average_loss = np.mean([min(d, 0) for d in self.__difference[:self.__period]])

        for d in self.__difference[self.__period:2 * self.__period]:
            self.__average_gain = (self.__average_gain * (self.__period - 1) + max(d, 0)) / self.__period
            self.__average_loss = (self.__average_loss * (self.__period - 1) + min(d, 0)) / self.__period

        self._values.append(100 - 100 / (1 + self.__average_gain / -self.__average_loss)) # XXX We'll need some kind of zero division protection

    def _next(self):
        self.__difference._update()

        input_index = len(self) + 2 * self.__period - 1
        if input_index >= len(self.__difference):
            raise StopIteration

        self.__average_gain = (self.__average_gain * (self.__period - 1) + max(self.__difference[input_index], 0)) / self.__period
        self.__average_loss = (self.__average_loss * (self.__period - 1) + min(self.__difference[input_index], 0)) / self.__period

        self._values.append(100 - 100 / (1 + self.__average_gain / -self.__average_loss))

def rsi(input_, period):
    return Rsi(input_, period)[:]
