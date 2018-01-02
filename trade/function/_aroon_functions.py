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

from trade.function import _Function

class AroonUpFunction(_Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

    def __len__(self):
        return max(len(self.input) - self.__period + 1, 0)

    def _calculate_values(self, count):
        count = min(count, len(self))
        if count <= 0:
            return []

        input_ = self.input[:self.__period + count - 1]

        high = (None, None)
        for i in range(0, self.__period - 1):
            if high[0] is not None and input_[i] > high[0] or high[0] is None:
                high = (input_[i], i)

        values = []
        for i in range(self.__period - 1, len(input_)):
            if high[0] is not None and input_[i] > high[0] or high[0] is None:
                high = (input_[i], i)

            if i - high[1] >= self.__period:
                high = (None, None)
                for j in range(i - self.__period + 1, i + 1):
                    if high[0] is not None and input_[j] > high[0] or high[0] is None:
                        high = (input_[j], j)

            values.append((self.__period - i + high[1]) / self.__period)

        return values

class AroonDownFunction(_Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

    def __len__(self):
        return max(len(self.input) - self.__period + 1, 0)

    def _calculate_values(self, count):
        count = min(count, len(self))
        if count <= 0:
            return []

        input_ = self.input[:self.__period + count - 1]

        low = (None, None)
        for i in range(0, self.__period - 1):
            if low[0] is not None and input_[i] < low[0] or low[0] is None:
                low = (input_[i], i)

        values = []
        for i in range(self.__period - 1, len(input_)):
            if low[0] is not None and input_[i] < low[0] or low[0] is None:
                low = (input_[i], i)

            if i - low[1] >= self.__period:
                low = (None, None)
                for j in range(i - self.__period + 1, i + 1):
                    if low[0] is not None and input_[j] < low[0] or low[0] is None:
                        low = (input_[j], j)

            values.append((self.__period - i + low[1]) / self.__period)

        return values

class AroonOscillatorFunction(_Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

    def __len__(self):
        return max(len(self.input) - self.__period + 1, 0)

    def _calculate_values(self, count):
        count = min(count, len(self))
        if count <= 0:
            return []

        input_ = self.input[:self.__period + count - 1]

        high = (None, None)
        low = (None, None)
        for i in range(0, self.__period - 1):
            if high[0] is not None and input_[i] > high[0] or high[0] is None:
                high = (input_[i], i)
            if low[0] is not None and input_[i] < low[0] or low[0] is None:
                low = (input_[i], i)

        values = []
        for i in range(self.__period - 1, len(input_)):
            if high[0] is not None and input_[i] > high[0] or high[0] is None:
                high = (input_[i], i)
            if low[0] is not None and input_[i] < low[0] or low[0] is None:
                low = (input_[i], i)

            if i - high[1] >= self.__period:
                high = (None, None)
                for j in range(i - self.__period + 1, i + 1):
                    if high[0] is not None and input_[j] > high[0] or high[0] is None:
                        high = (input_[j], j)

            if i - low[1] >= self.__period:
                low = (None, None)
                for j in range(i - self.__period + 1, i + 1):
                    if low[0] is not None and input_[j] < low[0] or low[0] is None:
                        low = (input_[j], j)

            aroon_up = (self.__period - i + high[1]) / self.__period
            aroon_down = (self.__period - i + low[1]) / self.__period
            values.append(aroon_up - aroon_down)

        return values
