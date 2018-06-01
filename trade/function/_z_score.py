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

class ZScore(Function):
    def __init__(self, input_, period):
        self.__input = FunctionInput(input_)
        self.__period = FunctionInput(period)

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.__period) or len(self) + int(self.__period.max) > len(self.__input):
            raise StopIteration

        self.inputs.sync({self.__input: int(self.__period.max)})

        latest_input = self.__input.consume()
        period = int(min(self.__period.consume(), self.__period.max))

        input_ = self.__input[self.__input.consumed - period:self.__input.consumed]
        mean = np.mean(input_)
        std = np.std(input_)

        self._values.append((latest_input - mean) / std)
