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

from trade.function import Function, Ema, Macd

class MacdHistogram(Function):
    def __init__(self, input_, short_period, long_period, signal_period):
        self.input = input_

        self.__macd = Macd(input_, short_period=short_period, long_period=long_period)
        self.__macd_signal = Ema(self.__macd, period=signal_period)

        Function.__init__(self)

    def _first(self):
        self._next()

    def _next(self):
        self.__macd._exhaust_input()
        self.__macd_signal._exhaust_input()

        if len(self.__macd_signal) == 0 or len(self) == len(self.__macd_signal):
            raise StopIteration

        offset = len(self.__macd) - len(self.__macd_signal)
        self._values.append(self.__macd[len(self) + offset] - self.__macd_signal[len(self)])
