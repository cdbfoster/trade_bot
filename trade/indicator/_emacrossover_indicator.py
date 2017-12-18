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

from trade.indicator import _Indicator, Signal

class EMACrossoverIndicator(_Indicator):
    def __init__(self, input_source, short_period, long_period):
        self.__input_source = input_source
        self.__short_period = short_period
        self.__long_period = long_period

        self.__short_ema = None
        self.__long_ema = None
        self.__initialize__()

    def get_signal(self):
        if self.__short_ema is None or self.__long_ema is None:
            if not self.__initialize__():
                return None

        difference = self.__short_ema - self.__long_ema
        return Signal.BUY if difference > 0 else Signal.SELL

    def update(self, steps=1):
        if self.__short_ema is None or self.__long_ema is None:
            self.__initialize__()
        else:
            short_weight = 2 / (self.__short_period + 1)
            long_weight = 2 / (self.__long_period + 1)

            for i in range(-steps, 0):
                self.__short_ema = _update_ema(self.__input_source[i], self.__short_ema, short_weight)
                self.__long_ema = _update_ema(self.__input_source[i], self.__long_ema, long_weight)

    def __initialize__(self):
        if len(self.__input_source) < 2 * self.__long_period:
            self.__short_ema = None
            self.__long_ema = None
            return False

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
