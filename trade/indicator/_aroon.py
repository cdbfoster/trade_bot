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

from trade.function import AroonOscillator
from trade.function.optimization import FloatParameter, IntParameter, Optimizable
from trade.indicator import Indicator, Signal

class AroonOscillatorCrossover(Indicator, Optimizable):
    def __init__(self, period):
        self.period = period

        self.__ao = AroonOscillator(period)

    def _first(self, x):
        self.__last_value = self.__ao._first(x)
        return Signal.HOLD

    def _next(self, x):
        this_value = self.__ao._next(x)
        last_value = self.__last_value

        self.__last_value = this_value

        if math.copysign(1, this_value) != math.copysign(1, last_value) and len(self) >= self.period:
            return Signal.BUY if this_value > 0 else Signal.SELL
        else:
            return Signal.HOLD

    def optimizable_parameters():
        return [
            IntParameter(minimum=2, maximum=10000), # period
        ]

class AroonOscillatorMinMax(Indicator, Optimizable):
    def __init__(self, period, fuzziness):
        self.period = period
        self.fuzziness = fuzziness

        self.__ao = AroonOscillator(period)

    def _first(self, x):
        self.__ao._first(x)
        return Signal.HOLD

    def _next(self, x):
        ao = self.__ao._next(x)
        if abs(ao) >= 100 * (1 - self.fuzziness) and len(self) >= self.period:
            return Signal.SELL if ao > 0 else Signal.BUY
        else:
            return Signal.HOLD

    def optimizable_parameters():
        return [
            IntParameter(minimum=2, maximum=10000),   # period
            FloatParameter(minimum=0.0, maximum=0.2), # fuzziness
        ]
