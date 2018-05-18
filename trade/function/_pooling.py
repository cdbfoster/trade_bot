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

class Close(Function):
    __input = FunctionInput()
    __period = FunctionInput()

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__input = input_
        self.__period = period

        self.__last_boundary = 0
        self.__last_period = None
        self.closes = []

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self.__period) == 0 or len(self) + int(self.__period.max) > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, int(self.__period.max))

        input_ = self.__input.consume()
        period = int(min(self.__period.consume(), self.__period.max))

        if self.__last_period is None:
            self.__last_period = period

        if (len(self) - self.__last_boundary) % self.__last_period > 0:
            self._values.append(self._values[-1])
        else:
            self.__last_boundary = len(self)
            self.__last_period = period
            self._values.append(input_)
            self.closes.append((self._values[-1], self.__last_boundary))

class High(Function):
    __input = FunctionInput()
    __period = FunctionInput()

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__input = input_
        self.__period = period

        self.__last_boundary = 0
        self.__last_period = None
        self.highs = []

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self.__period) == 0 or len(self) + int(self.__period.max) > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, int(self.__period.max))

        self.__input.consume()
        period = int(min(self.__period.consume(), self.__period.max))

        if self.__last_period is None:
            self.__last_period = period

        if (len(self) - self.__last_boundary) % self.__last_period > 0:
            self._values.append(self._values[-1])
        else:
            self.__last_boundary = len(self)
            self._values.append(max(self.__input[self.__input.consumed - self.__last_period:self.__input.consumed]))
            self.__last_period = period
            self.highs.append((self._values[-1], self.__last_boundary))

class Low(Function):
    __input = FunctionInput()
    __period = FunctionInput()

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__input = input_
        self.__period = period

        self.__last_boundary = 0
        self.__last_period = None
        self.lows = []

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self.__period) == 0 or len(self) + int(self.__period.max) > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, int(self.__period.max))

        self.__input.consume()
        period = int(min(self.__period.consume(), self.__period.max))

        if self.__last_period is None:
            self.__last_period = period

        if (len(self) - self.__last_boundary) % self.__last_period > 0:
            self._values.append(self._values[-1])
        else:
            self.__last_boundary = len(self)
            self._values.append(min(self.__input[self.__input.consumed - self.__last_period:self.__input.consumed]))
            self.__last_period = period
            self.lows.append((self._values[-1], self.__last_boundary))

class Open(Function):
    __input = FunctionInput()
    __period = FunctionInput()

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__input = input_
        self.__period = period

        self.__last_boundary = 0
        self.__last_period = None
        self.opens = []

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self.__period) == 0 or len(self) + int(self.__period.max) > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, int(self.__period.max))

        self.__input.consume()
        period = int(min(self.__period.consume(), self.__period.max))

        if self.__last_period is None:
            self.__last_period = period

        if (len(self) - self.__last_boundary) % self.__last_period > 0:
            self._values.append(self._values[-1])
        else:
            self.__last_boundary = len(self)
            self.__last_period = period
            self._values.append(self.__input[self.__input.consumed - period])
            self.opens.append((self._values[-1], self.__last_boundary))
