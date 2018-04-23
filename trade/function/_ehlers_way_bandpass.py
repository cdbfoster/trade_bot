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

from trade.function import Function

class EhlersWayBandpass(Function):
    def __init__(self, input_, period, delta):
        self.input = input_
        self.__period = period
        self.__delta = delta

        self.__beta = math.cos(2 * math.pi / self.__period)
        gamma = 1 / math.cos(4 * math.pi * self.__delta / self.__period)
        self.__alpha = gamma - math.sqrt(gamma * gamma - 1)

        Function.__init__(self)

    def _first(self):
        self.input._update()

        if len(self.input) < 5:
            raise StopIteration

        bp2 = 0.5 * (self.input[2] - self.input[0])
        bp1 = 0.5 * (1 - self.__alpha) * (self.input[3] - self.input[1]) + self.__beta * bp2
        bp = 0.5 * (1 - self.__alpha) * (self.input[4] - self.input[2]) + self.__beta * bp1 - self.__alpha * bp2

        self._values.append(bp1)
        self._values.append(bp)

    def _next(self):
        self.input._update()

        input_index = len(self) + 5 - 2;
        if input_index >= len(self.input):
            raise StopIteration

        self._values.append(0.5 * (1 - self.__alpha) * (self.input[input_index] - self.input[input_index - 2]) + self.__beta * (1 + self.__alpha) * self._values[-1] - self.__alpha * self._values[-2])

def ehlers_way_bandpass(input_, period, delta):
    return EhlersWayBandpass(input_, period, delta)[:]
