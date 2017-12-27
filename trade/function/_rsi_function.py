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

from trade.function import _Function, DifferenceFunction

class RsiFunction(_Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.__difference = DifferenceFunction(input_)

        self.__average_gain = None
        self.__average_loss = None

        self.__values = []
        self.__initialize()

    def __getitem__(self, index):
        return self.__values[index]

    def __len__(self):
        return len(self.__values)

    def update(self, steps=1, update_input=True):
        if update_input:
            self.input.update(steps)

        self.__difference.update(steps, update_input=False)

        if len(self.__values) == 0:
            self.__initialize()
        else:
            for i in range(-steps, 0):
                self.__average_gain = (self.__average_gain * (self.__period - 1) + max(self.__difference[i], 0)) / self.__period
                self.__average_loss = (self.__average_loss * (self.__period - 1) + min(self.__difference[i], 0)) / self.__period
                self.__values.append(self.__rsi())

    def __initialize(self):
        if len(self.__difference) < 2 * self.__period:
            return

        self.__average_gain = np.mean([max(self.__difference[i], 0) for i in range(self.__period)])
        self.__average_loss = np.mean([min(self.__difference[i], 0) for i in range(self.__period)])

        for i in range(self.__period, 2 * self.__period):
            self.__average_gain = (self.__average_gain * (self.__period - 1) + max(self.__difference[i], 0)) / self.__period
            self.__average_loss = (self.__average_loss * (self.__period - 1) + min(self.__difference[i], 0)) / self.__period

        self.__values.append(self.__rsi())

        for i in range(2 * self.__period, len(self.__difference)):
            self.__average_gain = (self.__average_gain * (self.__period - 1) + max(self.__difference[i], 0)) / self.__period
            self.__average_loss = (self.__average_loss * (self.__period - 1) + min(self.__difference[i], 0)) / self.__period
            self.__values.append(self.__rsi())

    def __rsi(self):
        return 100 - 100 / (1 + self.__average_gain / abs(self.__average_loss))
