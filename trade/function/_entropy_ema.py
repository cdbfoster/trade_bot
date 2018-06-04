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

from trade.function import Function, FunctionInput, ZScore

class EntropyEma(Function):
    def __init__(self, input_, period, zrange, alpha):
        self.__input = FunctionInput(input_)
        self.__period = FunctionInput(period)
        self.__zrange = FunctionInput(zrange)
        self.__alpha = FunctionInput(alpha)

        self.__zscore = FunctionInput(ZScore(input_, period))

        self.__entropy = 1.0
        self.__ema = 0

        Function.__init__(self)

    def _first(self):
        self.inputs.update()

        if len(self.__period) == 0 or int(self.__period.max) > len(self.__input): # XXX Add other inputs
            raise StopIteration

        self.inputs.sync({self.__input: int(self.__period.max)})

        self.__input.consume()
        period = int(min(self.__period.consume(), self.__period.max))
        self.__zrange.consume()
        self.__alpha.consume()

        self.__ema = np.mean(self.__input[self.__input.consumed - period:self.__input.consumed])
        self._values.append(self.__entropy)

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.__period) or len(self) + int(self.__period.max) > len(self.__input): # XXX
            raise StopIteration

        input_ = self.__input.consume()
        period = int(min(self.__period.consume(), self.__period.max))
        zrange = self.__zrange.consume()
        alpha = self.__alpha.consume()

        old_z = self.__zscore[self.__zscore.consumed - 1]
        z = self.__zscore.consume()

        action = max((abs(z) - abs(old_z)) / zrange, 0)
        if action > 0:
            self.__entropy = max(self.__entropy - action, 0)
        else:
            self.__entropy = 1 - (1 - self.__entropy) * alpha

        weight = 2 / (period + 1)

        #self._values.append((input_ - self._values[-1]) * weight + self._values[-1])
        self._values.append(self.__entropy)
