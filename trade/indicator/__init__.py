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

from enum import Enum

from trade.function import Function

class Signal(Enum):
    BUY = 1
    HOLD = 0
    SELL = -1

class Indicator(Function):
    def __init__(self):
        Function.__init__(self)

    def _first(self):
        self._next()

    def _next(self):
        pass

from ._aroonoscillator_indicator import AroonOscillatorIndicator
from ._emacrossover_indicator import EmaCrossoverIndicator
from ._macdsignalcrossover_indicator import MacdSignalCrossoverIndicator
from ._rsi_indicator import RsiIndicator
