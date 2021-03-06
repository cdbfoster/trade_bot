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

from trade.function import Atr, Function, FunctionInput, High, Low, Skip

class ChandelierExitLong(Function):
    def __init__(self, input_, pooling_period, period_count, multiplier):
        self.__period_count = FunctionInput(period_count)
        self.__multiplier = FunctionInput(multiplier)

        self.__high = FunctionInput(High(Skip(input_, 1), pooling_period))
        self.__atr = FunctionInput(Atr(input_, pooling_period, period_count))

        self.__current_period = 0
        self.__current_period_count = None

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= min(len(self.__atr), len(self.__high), len(self.__multiplier)):
            raise StopIteration

        self.inputs.sync()

        period_count = int(min(self.__period_count.consume(), self.__period_count.max))
        self.__high.consume()
        atr = self.__atr.consume()
        multiplier = self.__multiplier.consume()

        current_period = max(period + self.__current_period for period, (high, index) in enumerate(self.__high.highs[self.__current_period:]) if index < self.__high.consumed)
        if self.__current_period != current_period:
            self.__current_period = current_period
            self.__current_period_count = period_count

        period_high = max(high for high, _ in self.__high.highs[self.__current_period - self.__current_period_count + 1:self.__current_period + 1])
        self._values.append(period_high - atr * multiplier)

class ChandelierExitShort(Function):
    def __init__(self, input_, pooling_period, period_count, multiplier):
        self.__period_count = FunctionInput(period_count)
        self.__multiplier = FunctionInput(multiplier)

        self.__low = FunctionInput(Low(Skip(input_, 1), pooling_period))
        self.__atr = FunctionInput(Atr(input_, pooling_period, period_count))

        self.__current_period = 0
        self.__current_period_count = None

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= min(len(self.__atr), len(self.__low), len(self.__multiplier)):
            raise StopIteration

        self.inputs.sync()

        period_count = int(min(self.__period_count.consume(), self.__period_count.max))
        self.__low.consume()
        atr = self.__atr.consume()
        multiplier = self.__multiplier.consume()

        current_period = max(period + self.__current_period for period, (low, index) in enumerate(self.__low.lows[self.__current_period:]) if index < self.__low.consumed)
        if self.__current_period != current_period:
            self.__current_period = current_period
            self.__current_period_count = period_count

        period_low = min(low for low, _ in self.__low.lows[self.__current_period - self.__current_period_count + 1:self.__current_period + 1])
        self._values.append(period_low + atr * multiplier)
