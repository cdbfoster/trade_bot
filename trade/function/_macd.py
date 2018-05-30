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

from trade.function import Ema, Function, FunctionInput

class Macd(Function):
    def __init__(self, input_, period1, period2):
        self.__input = FunctionInput(input_)
        self.__period1 = FunctionInput(period1)
        self.__period2 = FunctionInput(period2)

        self.__ema1 = FunctionInput(Ema(input_, period1))
        self.__ema2 = FunctionInput(Ema(input_, period2))

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= min(len(self.__ema1), len(self.__ema2)):
            raise StopIteration

        self.inputs.sync_to_min_length()

        self.__input.consume()
        period1 = int(min(self.__period1.consume(), self.__period1.max))
        period2 = int(min(self.__period2.consume(), self.__period2.max))
        ema1 = self.__ema1.consume()
        ema2 = self.__ema2.consume()

        if period2 < period1:
            ema1, ema2 = ema2, ema1

        self._values.append(ema1 - ema2)

class MacdHistogram(Function):
    def __init__(self, input_, short_period, long_period, signal_period):
        self.input = input_

        self.__macd = Macd(input_, short_period=short_period, long_period=long_period)
        self.__macd_signal = Ema(self.__macd, period=signal_period)

        Function.__init__(self)

    def _next(self):
        self.__macd._update()
        self.__macd_signal._update()

        if len(self.__macd_signal) == 0 or len(self) == len(self.__macd_signal):
            raise StopIteration

        offset = len(self.__macd) - len(self.__macd_signal)
        self._values.append(self.__macd[len(self) + offset] - self.__macd_signal[len(self)])

def macd(input_, short_period, long_period):
    return Macd(input_, short_period, long_period)[:]

def macd_histogram(input_, short_period, long_period, signal_period):
    return MacdHistogram(input_, short_period, long_period, signal_period)[:]
