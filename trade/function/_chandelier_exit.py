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

from trade.function import Atr, High, Low, Skip

class ChandelierExitLong(Function):
    def __init__(self, input_, pooling_period, period_count, multiplier):
        self.input = input_
        self.__pooling_period = pooling_period
        self.__period_count = period_count
        self.__multiplier = multiplier

        self.__high = High(Skip(self.input, 1), self.__pooling_period)
        self.__atr = Atr(self.input, self.__pooling_period, self.__period_count)

        Function.__init__(self)

    def _next(self):
        self.__high._upate()
        self.__atr._update()

        if len(self) >= len(self.__atr):
            raise StopIteration

        current_period = len(self) // self.__pooling_period

        period_high = max(self.__high.highs[current_period:current_period + self.__period_count])
        self._values.append(period_high - self.__atr.atrs[current_period] * self.__multiplier)
