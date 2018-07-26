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

from . import optimization

class Function:
    def _first(self, x):
        raise NotImplementedError

    def _next(self, x):
        raise NotImplementedError

    def evaluate(self, x):
        if hasattr(self, "_Function__values"):
            result = self._next(x)
            self.__values.append(result)
        else:
            result = self._first(x)
            self.__values = [result]

        return result

    def evaluate_sequence(self, sequence):
        if len(sequence) == 0:
            return []

        try:
            start_index = len(self.__values)
        except AttributeError:
            self.__values = []
            start_index = 0

        if start_index == 0:
            self.__values.append(self._first(sequence[0]))

        for x in sequence[1 if start_index == 0 else 0:]:
            self.__values.append(self._next(x))

        return self.__values[start_index:]

    def __len__(self):
        try:
            return len(self.__values)
        except AttributeError:
            return 0

    def __getitem__(self, index):
        try:
            return self.__values[index]
        except AttributeError:
            return [][index]

    def __iter__(self):
        try:
            return iter(self.__values)
        except AttributeError:
            return iter([])

from ._ema import Ema, EmaDifference

#from ._arithmetic import Add, Divide, Multiply, Subtract
#from ._aroon import AroonUp, AroonDown, AroonOscillator
#from ._atr import Atr
#from ._change_period import ChangePeriod
#from ._ehlers_way_bandpass import EhlersWayBandpass
#from ._ema import Ema
#from ._historical_input import HistoricalInput
#from ._macd import Macd, MacdHistogram
#from ._pooling import Close, High, Low, Open
#from ._skip import Skip
#from ._chandelier_exit import ChandelierExitLong, ChandelierExitShort # Needs Atr, High, Low, Skip
#from ._slope import Slope
#from ._rsi import Rsi # Needs Slope
#from ._standard_deviation import StandardDeviation
#from ._dominant_band import DominantBand # Needs EhlersWayBandpass, StandardDeviation
#from ._z_score import ZScore
#from ._z_adjusted_ema import ZAdjustedEma # Needs ZScore
