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

from trade.function import Function, FunctionInput

class AroonUp(Function):
    __input = FunctionInput()
    __period = FunctionInput()

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__input = input_
        self.__period = period

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self) + int(self.__period.max) >= len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, int(self.__period.max))

        period = int(min(self.__period.consume(), self.__period.max))

        high = (None, None)
        for i in range(self.__input.consumed - period, self.__input.consumed + 1):
            if high[0] is not None and self.__input[i] > high[0] or high[0] is None:
                high = (self.__input[i], self.__input.consumed - i)

        self.__input.consume()

        self._values.append(100 * (period - high[1]) / period)

class AroonDown(Function):
    __input = FunctionInput()
    __period = FunctionInput()

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__input = input_
        self.__period = period

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self) + int(self.__period.max) >= len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, int(self.__period.max))

        period = int(min(self.__period.consume(), self.__period.max))

        low = (None, None)
        for i in range(self.__input.consumed - period, self.__input.consumed):
            if low[0] is not None and self.__input[i] < low[0] or low[0] is None:
                low = (self.__input[i], self.__input.consumed - i)

        self.__input.consume()

        self._values.append(100 * (period - low[1]) / period)

class AroonOscillator(Function):
    __up = FunctionInput()
    __down = FunctionInput()

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__up = AroonUp(input_, period)
        self.__down = AroonDown(input_, period)

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.__up):
            raise StopIteration

        self.inputs.sync_to_min_length()

        up = self.__up.consume()
        down = self.__down.consume()

        self._values.append(up - down)
