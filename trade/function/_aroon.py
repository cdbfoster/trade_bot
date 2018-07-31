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

from trade.function import Function

class AroonDown(Function):
    def __init__(self, period):
        self.period = period

    def _first(self, x):
        self.__low = x
        self.__low_index = 0
        self.__values = [x]
        self.__index = 0

        return 100

    def _next(self, x):
        if len(self.__values) == self.period + 1:
            self.__values[self.__index] = x
            self.__index += 1
            self.__index %= self.period + 1
        else:
            self.__values.append(x)

        if x < self.__low:
            self.__low = x
            self.__low_index = 0
        else:
            self.__low_index += 1

            if self.__low_index > self.period:
                self.__low_index = (self.__index - 1) % (self.period + 1)
                self.__low = self.__values[self.__low_index]

                for i in range(1, self.period + 1):
                    j = (self.__index - 1 - i) % (self.period + 1)

                    if self.__values[j] < self.__low:
                        self.__low = self.__values[j]
                        self.__low_index = j

        return 100 * (1 - self.__low_index / self.period)

class AroonOscillator(Function):
    def __init__(self, period):
        self.period = period

    def _first(self, x):
        self.__high = x
        self.__high_index = 0
        self.__low = x
        self.__low_index = 0
        self.__values = [x]
        self.__index = 0

        return 0

    def _next(self, x):
        if len(self.__values) == self.period + 1:
            self.__values[self.__index] = x
            self.__index += 1
            self.__index %= self.period + 1
        else:
            self.__values.append(x)

        if x > self.__high:
            self.__high = x
            self.__high_index = 0
        else:
            self.__high_index += 1

        if x < self.__low:
            self.__low = x
            self.__low_index = 0
        else:
            self.__low_index += 1

        find_high = self.__high_index > self.period
        find_low = self.__low_index > self.period

        if find_high:
            self.__high_index = (self.__index - 1) % (self.period + 1)
            self.__high = self.__values[self.__high_index]
        if find_low:
            self.__low_index = (self.__index - 1) % (self.period + 1)
            self.__low = self.__values[self.__low_index]

        if find_high or find_low:
            for i in range(1, self.period + 1):
                j = (self.__index - 1 - i) % (self.period + 1)

                if find_high and self.__values[j] > self.__high:
                    self.__high = self.__values[j]
                    self.__high_index = j

                if find_low and self.__values[j] < self.__low:
                    self.__low = self.__values[j]
                    self.__low_index = j

        return 100 * (self.__low_index - self.__high_index) / self.period

class AroonUp(Function):
    def __init__(self, period):
        self.period = period

    def _first(self, x):
        self.__high = x
        self.__high_index = 0
        self.__values = [x]
        self.__index = 0

        return 100

    def _next(self, x):
        if len(self.__values) == self.period + 1:
            self.__values[self.__index] = x
            self.__index += 1
            self.__index %= self.period + 1
        else:
            self.__values.append(x)

        if x > self.__high:
            self.__high = x
            self.__high_index = 0
        else:
            self.__high_index += 1

            if self.__high_index > self.period:
                self.__high_index = (self.__index - 1) % (self.period + 1)
                self.__high = self.__values[self.__high_index]

                for i in range(1, self.period + 1):
                    j = (self.__index - 1 - i) % (self.period + 1)

                    if self.__values[j] > self.__high:
                        self.__high = self.__values[j]
                        self.__high_index = j

        return 100 * (1 - self.__high_index / self.period)
