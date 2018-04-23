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

from trade.function import Subtract
from trade.indicator import Indicator, Signal

class Crossover(Indicator):
    def __init__(self, input1, input2=None, continuous=False):
        self.input = input1 if input2 is None else Subtract(input1, input2)
        self.input1 = input1
        self.input2 = input2
        self.__continuous = continuous

        Indicator.__init__(self)

    def _next(self):
        self.input._update()

        if len(self.input) < 2 or len(self) == len(self.input) - 1:
            raise StopIteration

        last_value = self.input[len(self)]
        this_value = self.input[len(self) + 1]

        if math.copysign(1, last_value) != math.copysign(1, this_value) or self.__continuous:
            self._values.append(Signal.BUY if this_value > 0 else Signal.SELL)
        else:
            self._values.append(Signal.HOLD)
