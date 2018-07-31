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

from trade.function import EmaDifference
from trade.function.optimization import IntParameter, Optimizable
from trade.indicator import Indicator, Signal

class EmaCrossover(Indicator, Optimizable):
    def __init__(self, short_period, long_period):
        if short_period >= long_period:
            raise ValueError

        self.short_period = short_period
        self.long_period = long_period

        self.__ema_difference = EmaDifference(short_period, long_period)

    def _first(self, x):
        self.__last_value = self.__ema_difference._first(x)
        return Signal.HOLD

    def _next(self, x):
        this_value = self.__ema_difference._next(x)
        last_value = self.__last_value

        self.__last_value = this_value

        if math.copysign(1, this_value) != math.copysign(1, last_value) and len(self) >= self.long_period:
            return Signal.BUY if this_value > 0 else Signal.SELL
        else:
            return Signal.HOLD

    def optimizable_parameters():
        return [
            IntParameter(minimum=3, maximum=15000), # short_period
            IntParameter(minimum=3, maximum=15000), # long_period
        ]
