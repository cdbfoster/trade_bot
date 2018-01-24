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

class AroonUp(Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        Function.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self) + self.__period - 1
        if input_index >= len(self.input):
            raise StopIteration

        high = (None, None)
        for i in range(len(self), len(self) + self.__period):
            if high[0] is not None and self.input[i] > high[0] or high[0] is None:
                high = (self.input[i], len(self) + self.__period - i)

        self._values.append(100 * (self.__period - high[1]) / self.__period)

class AroonDown(Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        Function.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self) + self.__period - 1
        if input_index >= len(self.input):
            raise StopIteration

        low = (None, None)
        for i in range(len(self), len(self) + self.__period):
            if low[0] is not None and self.input[i] < low[0] or low[0] is None:
                low = (self.input[i], len(self) + self.__period - i)

        self._values.append(100 * (self.__period - low[1]) / self.__period)

class AroonOscillator(Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.__up = AroonUp(self.input, self.__period)
        self.__down = AroonDown(self.input, self.__period)

        Function.__init__(self)

    def _next(self):
        self.__up._update()
        self.__down._update()

        if len(self.__up) == 0 or len(self) == len(self.__up):
            raise StopIteration

        self._values.append(self.__up[len(self)] - self.__down[len(self)])

class PeriodAdjustedAroonOscillator(Function):
    def __init__(self, input_, period_function, max_period):
        self.input = input_
        self.__period = period_function
        self.__max_period = max_period

        Function.__init__(self)

    def _next(self):
        self.__period._update()
        self.input._update()

        input_index = len(self) + self.__max_period
        if len(self) >= len(self.__period)  or input_index > len(self.input):
            raise StopIteration

        period = int(self.__period[len(self)])
        input_ = self.input[input_index - period:input_index]
        up = aroon_up(input_, period)[0]
        down = aroon_down(input_, period)[0]

        self._values.append(up - down)

def aroon_up(input_, period):
    return AroonUp(input_, period)[:]

def aroon_down(input_, period):
    return AroonDown(input_, period)[:]

def aroon_oscillator(input_, period):
    return AroonOscillator(input_, period)[:]
