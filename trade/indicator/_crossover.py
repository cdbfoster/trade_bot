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
from trade.indicator import Indicator, IndicatorInput, Signal

class Crossover(Indicator):
    def __init__(self, input1, input2=None, continuous=False):
        self.__input1 = IndicatorInput(input1)
        self.__input2 = IndicatorInput(input2) if input2 is not None else None
        self.__continuous = continuous

        self.__input = self.__input1 if input2 is None else IndicatorInput(Subtract(input1, input2))

        Indicator.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) + 2 > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, 2)

        last_value = self.__input[self.__input.consumed - 1]
        this_value = self.__input.consume()

        if math.copysign(1, last_value) != math.copysign(1, this_value) or self.__continuous:
            self._values.append(Signal.BUY if this_value > 0 else Signal.SELL)
        else:
            self._values.append(Signal.HOLD)
