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

from trade.function import Rsi as RsiFunction
from trade.function.optimization import FloatParameter, IntParameter, Optimizable
from trade.indicator import Indicator, Signal

class Rsi(Indicator, Optimizable):
    def __init__(self, period, threshold):
        self.period = period
        self.threshold = threshold

        self.__rsi = RsiFunction(period)

    def _first(self, x):
        self.__rsi._first(x)
        return Signal.HOLD

    def _next(self, x):
        rsi = self.__rsi._next(x)

        if rsi < self.threshold and len(self) >= self.period:
            return Signal.BUY
        elif rsi > 100 - self.threshold and len(self) >= self.period:
            return Signal.SELL
        else:
            return Signal.HOLD

    def optimizable_parameters():
        return [
            IntParameter(minimum=2, maximum=10000), # period
            FloatParameter(minimum=1, maximum=50),  # threshold
        ]
