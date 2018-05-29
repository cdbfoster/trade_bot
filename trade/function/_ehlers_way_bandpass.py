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

import math

from trade.function import Function, FunctionInput

class EhlersWayBandpass(Function):
    def __init__(self, input_, period, delta):
        self.__input = FunctionInput(input_)
        self.__period = FunctionInput(period)
        self.__delta = FunctionInput(delta)

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self.__period) == 0 or len(self.__delta) == 0 or len(self) + 5 > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_min_length()

        period = self.__period.consume()
        delta = self.__delta.consume()

        beta = math.cos(2 * math.pi / period)
        gamma = 1 / math.cos(4 * math.pi * delta / period)
        alpha = gamma - math.sqrt(gamma * gamma - 1)

        i = self.__input.consumed
        bp2 = self._values[-min(len(self), 2)] if len(self) >= 1 else 0.5 * (1 - alpha) * (self.__input[i - 2] - self.__input[i - 4]) + beta * (1 + alpha) * (self.__input[i - 2] - self.__input[i - 4]) - alpha * (self.__input[i - 2] - self.__input[i - 4])
        bp1 = self._values[-1] if len(self) >= 2 else 0.5 * (1 - alpha) * (self.__input[i - 1] - self.__input[i - 3]) + beta * (1 + alpha) * (self.__input[i - 1] - self.__input[i - 3]) - alpha * bp2
        bp = 0.5 * (1 - alpha) * (self.__input[i] - self.__input[i - 2]) + beta * (1 + alpha) * bp1 - alpha * bp2

        self._values.append(bp)
        self.__input.consume()
