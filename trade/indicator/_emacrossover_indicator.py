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

import numpy as np

from trade.indicator import Indicator, Signal

class EmaCrossoverIndicator(Indicator):
    def __init__(self, input_source, short_period, long_period, debug=None):
        self.__input_source = input_source
        self.__short_period = short_period
        self.__long_period = long_period
        self.debug = debug

        if self.debug is not None:
            self.debug.write("input short long signal\n")

        self.__short_ema = None
        self.__long_ema = None
        self.__initialize__()

        self.__old_signal = None

    def get_signal(self):
        if self.__short_ema is None or self.__long_ema is None:
            if not self.__initialize__():
                return None

        new_signal = Signal.BUY if self.__short_ema - self.__long_ema > 0 else Signal.SELL
        return new_signal if new_signal != self.__old_signal else Signal.HOLD

    def update(self, steps=1):
        if self.__short_ema is None or self.__long_ema is None:
            self.__initialize__()
        else:
            for i in range(-steps, 0):
                self.__old_signal = Signal.BUY if self.__short_ema - self.__long_ema > 0 else Signal.SELL
                self.__short_ema = _update_ema(self.__input_source[i], self.__short_ema, self.__short_weight)
                self.__long_ema = _update_ema(self.__input_source[i], self.__long_ema, self.__long_weight)

                if self.debug is not None:
                    signal = self.get_signal()
                    self.debug.write("{} {} {} {}\n".format(
                        self.__input_source[i],
                        self.__short_ema,
                        self.__long_ema,
                        signal.value if signal is not None else 0,
                    ))

    def __initialize__(self):
        if len(self.__input_source) < 2 * self.__long_period:
            self.__short_ema = None
            self.__long_ema = None
            return False

        self.__short_weight = 2 / (self.__short_period + 1)
        self.__long_weight = 2 / (self.__long_period + 1)

        self.__short_ema = _ema(self.__input_source, self.__short_period)
        self.__long_ema = _ema(self.__input_source, self.__long_period)

        return True

def _ema(values, period):
    ema = np.mean(values[:period])
    weight = 2 / (period + 1)

    for x in values[period:]:
        ema = _update_ema(x, ema, weight)

    return ema

def _update_ema(value, current, weight):
    return (value - current) * weight + current
