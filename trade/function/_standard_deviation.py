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

        Function.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self) + self.__period - 1
        if input_index >= len(self.input):
            raise StopIteration

        input_ = self.input[input_index - self.__period + 1:input_index + 1]
        self._values.append(np.std(input_))

def standard_deviation(input_, period):
    return StandardDeviation(input_, period)[:]
