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

from trade.indicator import Indicator, Signal

class MacdSignalCrossoverIndicator(Indicator):
    def __init__(self, input_source, short_period=320, long_period=720, signal_period=250, debug=None):
        self.__input_source = input_source
        self.__short_period = short_period
        self.__long_period = long_period
        self.__signal_period = signal_period
        self.debug = debug

        if self.debug is not None:
            self.debug.write("input short long macd macd-signal macd-hist signal\n")

        self.__short_ema = None
        self.__long_ema = None
        self.__signal_ema = None
        self.__initialize__()

        self.__old_macd_hist = None

    def get_signal(self):
        if self.__short_ema is None or self.__long_ema is None or self.__signal_ema is None:
            if not self.__initialize__():
                return None

        macd_hist = self.__short_ema - self.__long_ema - self.__signal_ema
        if math.copysign(1, macd_hist) != math.copysign(1, self.__old_macd_hist):
            return Signal.BUY if macd_hist >= 0 else Signal.SELL
            #if self.__signal_ema < 0:
            #    return Signal.BUY if macd_hist >= 0 else Signal.HOLD
            #else:
            #    return Signal.SELL if macd_hist < 0 else Signal.HOLD
        return Signal.HOLD

    def update(self, steps=1):
        if self.__short_ema is None or self.__long_ema is None or self.__signal_ema is None:
            self.__initialize__()
        else:
            for i in range(-steps, 0):
                self.__old_macd_hist = self.__short_ema - self.__long_ema - self.__signal_ema
                self.__short_ema = _update_ema(self.__input_source[i], self.__short_ema, self.__short_weight)
                self.__long_ema = _update_ema(self.__input_source[i], self.__long_ema, self.__long_weight)
                self.__signal_ema = _update_ema(self.__short_ema - self.__long_ema, self.__signal_ema, self.__signal_weight)

                if self.debug is not None:
                    signal = self.get_signal()
                    self.debug.write("{} {} {} {} {} {} {}\n".format(
                        self.__input_source[i],
                        self.__short_ema,
                        self.__long_ema,
                        self.__short_ema - self.__long_ema,
                        self.__signal_ema,
                        self.__short_ema - self.__long_ema - self.__signal_ema,
                        signal.value if signal is not None else 0,
                    ))

    def __initialize__(self):
        if len(self.__input_source) < 2 * self.__long_period + 2 * self.__signal_period:
            self.__short_ema = None
            self.__long_ema = None
            self.__signal_ema = None
            return False

        self.__short_weight = 2 / (self.__short_period + 1)
        self.__long_weight = 2 / (self.__long_period + 1)
        self.__signal_weight = 2 / (self.__signal_period + 1)

        initial_data = self.__input_source[:-2 * self.__signal_period]
        self.__short_ema = _ema(initial_data, self.__short_period)
        self.__long_ema = _ema(initial_data, self.__long_period)

        sma = 0
        for i in range(-2 * self.__signal_period, -self.__signal_period):
            self.__short_ema = _update_ema(self.__input_source[i], self.__short_ema, self.__short_weight)
            self.__long_ema = _update_ema(self.__input_source[i], self.__long_ema, self.__long_weight)
            sma += self.__short_ema - self.__long_ema
        sma /= self.__signal_period
        self.__signal_ema = sma

        # Don't write to the debug file during initialization
        debug = self.debug
        self.debug = None
        self.update(steps=self.__signal_period)
        self.debug = debug

        return True

def _ema(values, period):
    ema = np.mean(values[:period])
    weight = 2 / (period + 1)

    for x in values[period:]:
        ema = _update_ema(x, ema, weight)

    return ema

def _update_ema(value, current, weight):
    return (value - current) * weight + current
