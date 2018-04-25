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

class Close(Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.closes = []

        Function.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self) + self.__period - 1
        if input_index >= len(self.input):
            raise StopIteration

        current_period = len(self) // self.__period

        if current_period < len(self.closes):
            self._values.append(self._values[-1])
        else:
            self._values.append(self.input[input_index])
            self.closes.append(self._values[-1])

class High(Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.highs = []

        Function.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self) + self.__period - 1
        if input_index >= len(self.input):
            raise StopIteration

        current_period = len(self) // self.__period

        if current_period < len(self.highs):
            self._values.append(self._values[-1])
        else:
            self._values.append(max(self.input[input_index - self.__period + 1:input_index + 1]))
            self.highs.append(self._values[-1])

class Low(Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.lows = []

        Function.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self) + self.__period - 1
        if input_index >= len(self.input):
            raise StopIteration

        current_period = len(self) // self.__period

        if current_period < len(self.lows):
            self._values.append(self._values[-1])
        else:
            self._values.append(min(self.input[input_index - self.__period + 1:input_index + 1]))
            self.lows.append(self._values[-1])

class Open(Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.opens = []

        Function.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self) + self.__period - 1
        if input_index >= len(self.input):
            raise StopIteration

        current_period = len(self) // self.__period

        if current_period < len(self.opens):
            self._values.append(self._values[-1])
        else:
            self._values.append(self.input[input_index - self.__period + 1])
            self.opens.append(self._values[-1])
