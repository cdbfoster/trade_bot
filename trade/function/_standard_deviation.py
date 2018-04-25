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

class StandardDeviation(Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.__mean = 0.0
        self.__error_sum = 0.0
        self.__variance = 0.0

        Function.__init__(self)

    def _first(self):
        self.input._update()

        if len(self.input) < self.__period:
            raise StopIteration

        input_ = np.array(self.input[:self.__period])
        self.__mean = np.mean(input_)
        self.__error_sum = np.sum((input_ - self.__mean) ** 2)
        self.__variance = self.__error_sum / self.__period

        self._values.append(np.sqrt(self.__variance))

    def _next(self):
        self.input._update()

        input_index = len(self) + self.__period - 1
        if input_index >= len(self.input):
            raise StopIteration

        value_discard = self.input[len(self) - 1]
        value_new = self.input[input_index]

        delta_new_discard = value_new - value_discard
        delta_discard_mean = value_discard - self.__mean

        delta_new_mean_before = value_new - self.__mean
        self.__mean += delta_new_discard / self.__period
        delta_new_mean_after = value_new - self.__mean

        self.__error_sum -= ((delta_discard_mean * delta_discard_mean - delta_new_mean_before * delta_new_mean_after) * self.__period +
            delta_new_discard * delta_new_mean_after) / (self.__period - 1)
        self.__variance = abs(self.__error_sum / self.__period)

        self._values.append(np.sqrt(self.__variance))

def standard_deviation(input_, period):
    return StandardDeviation(input_, period)[:]
