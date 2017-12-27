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

from trade.function import _Function

class EmaFunction(_Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.__weight = 2 / (self.__period + 1)

        self.__values = []
        self.__initialize()

    def __getitem__(self, index):
        return self.__values[index]

    def __len__(self):
        return len(self.__values)

    def update(self, steps=1, update_input=True):
        if update_input:
            self.input.update(steps)

        if len(self.__values) == 0:
            self.__initialize()
        else:
            for i in range(-steps, 0):
                self.__values.append(self.__update_ema(self.input[i], self.__values[-1]))

    def __initialize(self):
        if len(self.input) < 2 * self.__period:
            return

        ema = np.mean(self.input[:self.__period])
        for x in self.input[self.__period:2 * self.__period]:
            ema = self.__update_ema(x, ema)

        self.__values.append(ema)
        for i in range(2 * self.__period, len(self.input)):
            self.__values.append(self.__update_ema(self.input[i], self.__values[-1]))

    def __update_ema(self, value, current):
        return (value - current) * self.__weight + current
