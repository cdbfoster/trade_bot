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
    pass

from ._benchmark import Benchmark
from ._aroon import AroonOscillatorCrossover, AroonOscillatorMinMax
from ._ema_crossover import EmaCrossover

#from ._crossover import Crossover
#from ._logic import And, Not, Or
#from ._min_max import MinMax
#from ._threshold import Threshold
