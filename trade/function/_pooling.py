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

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__input = input_
        self.__period = int(period)

        self.closes = []

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self) + self.__period > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, self.__period)

        input_ = self.__input.consume()

        if len(self) % self.__period > 0:
            self._values.append(self._values[-1])
        else:
            self._values.append(input_)
            self.closes.append(self._values[-1])

class High(Function):
    __input = FunctionInput()

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__input = input_
        self.__period = int(period)

        self.highs = []

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self) + self.__period > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, self.__period)

        self.__input.consume()

        if len(self) % self.__period > 0:
            self._values.append(self._values[-1])
        else:
            self._values.append(max(self.__input[len(self.highs) * self.__period:(len(self.highs) + 1) * self.__period]))
            self.highs.append(self._values[-1])

class Low(Function):
    __input = FunctionInput()

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__input = input_
        self.__period = int(period)

        self.lows = []

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self) + self.__period > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, self.__period)

        self.__input.consume()

        if len(self) % self.__period > 0:
            self._values.append(self._values[-1])
        else:
            self._values.append(min(self.__input[len(self.lows) * self.__period:(len(self.lows) + 1) * self.__period]))
            self.lows.append(self._values[-1])

class Open(Function):
    __input = FunctionInput()

    def __init__(self, input_, period):
        Function.__init__(self)
        self.__input = input_
        self.__period = int(period)

        self.opens = []

        self._update()

    def _next(self):
        self.inputs.update()

        if len(self) + self.__period > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, self.__period)

        self.__input.consume()

        if len(self) % self.__period > 0:
            self._values.append(self._values[-1])
        else:
            self._values.append(self.__input[len(self.opens) * self.__period])
            self.opens.append(self._values[-1])
