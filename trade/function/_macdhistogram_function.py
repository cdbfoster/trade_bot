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

from trade.function import _Function, EmaFunction, MacdFunction

class MacdHistogramFunction(_Function):
    def __init__(self, input_, short_period, long_period, signal_period):
        self.input = input_

        self.__macd = MacdFunction(input_, short_period=short_period, long_period=long_period)
        self.__macd_signal = EmaFunction(self.__macd, period=signal_period)

    def __len__(self):
        return len(self.__macd_signal)

    def _calculate_values(self, count):
        count = min(count, len(self))
        if count <= 0:
            return []

        start = -len(self)
        macd = self.__macd[start:start + count if start + count < 0 else None]
        macd_signal = self.__macd_signal[start:start + count if start + count < 0 else None]

        return list(m - s for m, s in zip(macd, macd_signal))
