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

from trade.function import Function

class ZeroLagMa(Function):
    def __init__(self, input_, ema_period, gain_limit):
        self.input = input_
        self.__ema_period = ema_period
        self.__gain_limit = gain_limit
        self.__weight = 2 / (self.__ema_period + 1)

        self.__ema = None

        Function.__init__(self)

    def _first(self):
        self.input._update()

        if len(self.input) < 2 * self.__ema_period:
            raise StopIteration

        self.__ema = np.mean(self.input[:self.__ema_period])
        ec = None
        for x in self.input[self.__ema_period: 2 * self.__ema_period - 1]:
            self.__ema = (x - self.__ema) * self.__weight + self.__ema
            ec = self.__error_corrected_ema(x, self.__ema, ec if ec is not None else self.__ema)

        self.__ema = (self.input[2 * self.__ema_period - 1] - self.__ema) * self.__weight + self.__ema
        self._values.append(self.__error_corrected_ema(self.input[2 * self.__ema_period - 1], self.__ema, ec))

    def _next(self):
        self.input._update()

        input_index = len(self) + 2 * self.__ema_period - 1
        if input_index >= len(self.input):
            raise StopIteration

        self.__ema = (self.input[2 * self.__ema_period - 1] - self.__ema) * self.__weight + self.__ema
        self._values.append(self.__error_corrected_ema(self.input[input_index], self.__ema, self._values[-1]))

    def __error_corrected_ema(self, x, ema, previous_ec):
        gain = (x + previous_ec - self.__weight * (previous_ec - ema)) / (self.__weight * (x - previous_ec))

        print(gain)
        gain = min(max(gain, -self.__gain_limit), self.__gain_limit)

        """
        least_error = 1000000
        gain = None
        for current_gain in np.linspace(-self.__gain_limit, self.__gain_limit, int(2 * self.__gain_limit * 10) + 1):
            ec = self.__weight * (x + current_gain * (x - previous_ec)) + (1 - self.__weight) * previous_ec
            error = x - ec
            if abs(error) < least_error:
                least_error = abs(error)
                gain = current_gain
        #"""

        print(gain)

        gain = 50

        return self.__weight * (x + gain * (x - previous_ec)) + (1 - self.__weight) * previous_ec

def zero_lag_ma(input_, ema_period, gain_limit):
    return ZeroLagMa(input_, ema_period, gain_limit)[:]

# 0 = c - a * (e + g * (c - f)) + (1 - a) * f
# c + (1 - a) * f = a * e + a * g * (c - f)
# c + (1 - a) * f - a * e = a * g * (c - f)
# (c + (1 - a) * f - a * e) / (a * (c - f)) = g
# (c + f - af - ae) / (ac - af) = g
