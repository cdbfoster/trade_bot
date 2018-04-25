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

class Atr(Function):
    def __init__(self, input_, pooling_period, period_count):
        self.input = input_
        self.__pooling_period = pooling_period
        self.__period_count = period_count

        self.__trs = []
        self.atrs = []

        Function.__init__(self)

    def _first(self):
        self.input._update()

        if len(self.input) < self.__pooling_period * self.__period_count + 1:
            raise StopIteration

        for period in range(self.__period_count):
            input_ = self.input[period * self.__pooling_period + 1:(period + 1) * self.__pooling_period + 1]
            high = max(input_)
            low = min(input_)
            close = self.input[period * self.__pooling_period]

            self.__trs.append(max(high - low, abs(high - close), abs(low - close)))

        self._values.append(np.mean(self.__trs))
        self.atrs.append(self._values[-1])

    def _next(self):
        self.input._update()

        input_index = len(self) + self.__pooling_period * self.__period_count
        if input_index >= len(self.input):
            raise StopIteration

        current_period = len(self) // self.__pooling_period + self.__period_count - 1

        if current_period < len(self.__trs):
            self._values.append(self._values[-1])
        else:
            input_ = self.input[current_period * self.__pooling_period + 1:(current_period + 1) * self.__pooling_period + 1]
            high = max(input_)
            low = min(input_)
            close = self.input[current_period * self.__pooling_period]

            self.__trs.append(max(high - low, abs(high - close), abs(low - close)))
            self._values.append((self._values[-1] * (self.__period_count - 1) + self.__trs[-1]) / self.__period_count)
            self.atrs.append(self._values[-1])

def atr(input_, pooling_period, period_count):
    return Atr(input_, pooling_period, period_count)[:]
