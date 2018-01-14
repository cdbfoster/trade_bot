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

from trade.function import Function

class EmaFunction(Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period
        self.__weight = 2 / (self.__period + 1)

        Function.__init__(self)

    def _first(self):
        if len(self.input) < 2 * self.__period:
            raise StopIteration

        ema = np.mean(self.input[:self.__period])
        for x in self.input[self.__period: 2 * self.__period - 1]:
            ema = (x - ema) * self.__weight + ema

        self._values.append((self.input[2 * self.__period - 1] - ema) * self.__weight + ema)

    def _next(self):
        input_index = len(self) + 2 * self.__period - 1
        if input_index >= len(self.input):
            raise StopIteration

        self._values.append((self.input[input_index] - self._values[-1]) * self.__weight + self._values[-1])
