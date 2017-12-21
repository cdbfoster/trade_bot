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
import numpy as np

from trade.indicator import _Indicator, Signal

class RSIIndicator(_Indicator):
    def __init__(self, input_source, period=14, overbought_threshold=0.7, oversold_threshold=0.3, debug=None):
        self.__input_source = input_source
        self.__period = period
        self.__overbought_threshold = overbought_threshold
        self.__oversold_threshold = oversold_threshold
        self.debug = debug

        if self.debug is not None:
            self.debug.write("input rsi signal\n");

        self.__average_gain = None
        self.__average_loss = None
        self.__initialize__()

    def get_signal(self):
        if self.__average_gain is None or self.__average_loss is None:
            if not self.__initialize__():
                return None

        rsi = 1 - 1 / (1 + self.__average_gain / abs(self.__average_loss))
        if rsi > self.__overbought_threshold:
            return Signal.SELL
        elif rsi < self.__oversold_threshold:
            return Signal.BUY
        else:
            return Signal.HOLD

    def update(self, steps=1):
        if self.__average_gain is None or self.__average_loss is None:
            self.__initialize__()
        else:
            for i in range(-steps, 0):
                difference = self.__input_source[i] - self.__input_source[i - 1]
                self.__average_gain = (self.__average_gain * (self.__period - 1) + max(difference, 0)) / self.__period
                self.__average_loss = (self.__average_loss * (self.__period - 1) + min(difference, 0)) / self.__period

                if self.debug is not None:
                    signal = self.get_signal()
                    self.debug.write("{} {} {}\n".format(
                        self.__input_source[i],
                        1 - 1 / (1 + self.__average_gain / abs(self.__average_loss)),
                        signal.value if signal is not None else 0,
                    ))

    def __initialize__(self):
        if len(self.__input_source) < 2 * self.__period + 1:
            self.__average_gain = None
            self.__average_loss = None
            return False

        differences = [self.__input_source[i + 1] - self.__input_source[i] for i in range(len(self.__input_source) - 1)]
        self.__average_gain = np.mean([max(x, 0) for x in differences[:self.__period]])
        self.__average_loss = np.mean([min(x, 0) for x in differences[:self.__period]])

        for x in differences[self.__period:]:
            self.__average_gain = (self.__average_gain * (self.__period - 1) + max(x, 0)) / self.__period
            self.__average_loss = (self.__average_loss * (self.__period - 1) + min(x, 0)) / self.__period
