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

from trade.function import Function, FunctionInput

class Atr(Function):
    def __init__(self, input_, pooling_period, period_count):
        self.__input = FunctionInput(input_)
        self.__pooling_period = FunctionInput(pooling_period)
        self.__period_count = FunctionInput(period_count)

        self.__last_pool_boundary = None
        self.__last_pooling_period = None
        self.__trs = []
        self.atrs = []

        Function.__init__(self)

    def _first(self):
        self.inputs.update()

        if min(len(self.__pooling_period), len(self.__period_count)) == 0 or int(self.__pooling_period.max) * int(self.__period_count.max) + 1 > len(self.__input):
            raise StopIteration

        self.inputs.sync({self.__input: int(self.__pooling_period.max) * int(self.__period_count.max) + 1})

        self.__input.consume()
        pooling_period = int(min(self.__pooling_period.consume(), self.__pooling_period.max))
        period_count = int(max(min(self.__period_count.consume(), self.__period_count.max), 1))

        for period in range(period_count):
            input_ = self.__input[self.__input.consumed - (period_count - period) * pooling_period:self.__input.consumed - (period_count - period - 1) * pooling_period]
            high = max(input_)
            low = min(input_)
            close = self.__input[self.__input.consumed - (period_count - period) * pooling_period - 1]

            self.__trs.append(max(high - low, abs(high - close), abs(low - close)))

        self.__last_pool_boundary = 0
        self.__last_pooling_period = pooling_period
        self._values.append(np.mean(self.__trs))
        self.atrs.append(self._values[-1])

    def _next(self):
        self.inputs.update()

        if len(self) >= min(len(self.__pooling_period), len(self.__period_count)) or len(self) + int(self.__pooling_period.max) * int(self.__period_count.max) + 1 > len(self.__input):
            raise StopIteration

        self.__input.consume()
        pooling_period = int(min(self.__pooling_period.consume(), self.__pooling_period.max))
        period_count = int(max(min(self.__period_count.consume(), self.__period_count.max), 1))

        if len(self) - self.__last_pool_boundary < self.__last_pooling_period:
            self._values.append(self._values[-1])
        else:
            input_ = self.__input[self.__input.consumed - self.__last_pooling_period:self.__input.consumed]
            high = max(input_)
            low = min(input_)
            close = self.__input[self.__input.consumed - self.__last_pooling_period - 1]

            self.__last_pool_boundary = len(self)
            self.__last_pooling_period = pooling_period
            self.__trs.append(max(high - low, abs(high - close), abs(low - close)))
            self._values.append((self._values[-1] * (period_count - 1) + self.__trs[-1]) / period_count)
            self.atrs.append(self._values[-1])
