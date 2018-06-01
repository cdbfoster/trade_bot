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

class StandardDeviation(Function):
    def __init__(self, input_, period):
        self.__input = FunctionInput(input_)
        self.__period = FunctionInput(period)

        self.__mean = 0.0
        self.__error_sum = 0.0
        self.__variance = 0.0

        Function.__init__(self)

    def _first(self):
        self.inputs.update()

        if len(self.__period) == 0 or int(self.__period.max) > len(self.__input):
            raise StopIteration

        self.inputs.sync({self.__input: int(self.__period.max)})

        self.__input.consume()
        period = int(min(self.__period.consume(), self.__period.max))

        input_ = np.array(self.__input[self.__input.consumed - period:self.__input.consumed])
        self.__mean = np.mean(input_)
        self.__error_sum = np.sum((input_ - self.__mean) ** 2)
        self.__variance = self.__error_sum / period

        self._values.append(np.sqrt(self.__variance))

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.__period) or len(self) + int(self.__period.max) > len(self.__input):
            raise StopIteration

        value_discard = self.__input[self.__input.consumed - 1]
        value_new = self.__input.consume()
        period_discard = int(min(self.__period[self.__period.consumed - 1], self.__period.max))
        period_new = int(min(self.__period.consume(), self.__period.max))

        delta_new_discard = value_new - value_discard
        delta_discard_mean = value_discard - self.__mean

        delta_new_mean_before = value_new - self.__mean
        self.__mean += delta_new_discard / period_new
        delta_new_mean_after = value_new - self.__mean

        self.__error_sum -= ((delta_discard_mean * delta_discard_mean - delta_new_mean_before * delta_new_mean_after) * period_discard +
            delta_new_discard * delta_new_mean_after) / (period_discard - 1)
        self.__variance = abs(self.__error_sum / period_new)

        self._values.append(np.sqrt(self.__variance))
