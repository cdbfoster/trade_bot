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

class Add(Function):
    def __init__(self, input1, input2):
        self.input = input1
        self.input1 = input1
        self.input2 = input2

        Function.__init__(self)

    def _next(self):
        self.input1._update()
        self.input2._update()

        input1_shift = max(len(self.input1) - len(self.input2), 0)
        input2_shift = max(len(self.input2) - len(self.input1), 0)

        input_index = len(self)
        if input_index + input1_shift >= len(self.input1) or input_index + input2_shift >= len(self.input2):
            raise StopIteration

        self._values.append(self.input1[input_index + input1_shift] + self.input2[input_index + input2_shift])

class Divide(Function):
    def __init__(self, input1, input2):
        self.input = input1
        self.input1 = input1
        self.input2 = input2

        Function.__init__(self)

    def _next(self):
        self.input1._update()
        self.input2._update()

        input1_shift = max(len(self.input1) - len(self.input2), 0)
        input2_shift = max(len(self.input2) - len(self.input1), 0)

        input_index = len(self)
        if input_index + input1_shift >= len(self.input1) or input_index + input2_shift >= len(self.input2):
            raise StopIteration

        self._values.append(self.input1[input_index + input1_shift] / (self.input2[input_index + input2_shift] if self.input2[input_index + input2_shift] != 0.0 else 0.00000001))

class Multiply(Function):
    def __init__(self, input1, input2):
        self.input = input1
        self.input1 = input1
        self.input2 = input2

        Function.__init__(self)

    def _next(self):
        self.input1._update()
        self.input2._update()

        input1_shift = max(len(self.input1) - len(self.input2), 0)
        input2_shift = max(len(self.input2) - len(self.input1), 0)

        input_index = len(self)
        if input_index + input1_shift >= len(self.input1) or input_index + input2_shift >= len(self.input2):
            raise StopIteration

        self._values.append(self.input1[input_index + input1_shift] * self.input2[input_index + input2_shift])

class Offset(Function):
    def __init__(self, input_, value):
        self.input = input_
        self.__value = value

        Function.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self)
        if input_index >= len(self.input):
            raise StopIteration

        self._values.append(self.input[input_index] + self.__value)

class Scale(Function):
    def __init__(self, input_, value):
        self.input = input_
        self.__value = value

        Function.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self)
        if input_index >= len(self.input):
            raise StopIteration

        self._values.append(self.input[input_index] * self.__value)

class Subtract(Function):
    def __init__(self, input1, input2):
        self.input = input1
        self.input1 = input1
        self.input2 = input2

        Function.__init__(self)

    def _next(self):
        self.input1._update()
        self.input2._update()

        input1_shift = max(len(self.input1) - len(self.input2), 0)
        input2_shift = max(len(self.input2) - len(self.input1), 0)

        input_index = len(self)
        if input_index + input1_shift >= len(self.input1) or input_index + input2_shift >= len(self.input2):
            raise StopIteration

        self._values.append(self.input1[input_index + input1_shift] - self.input2[input_index + input2_shift])

def add(input1, input2):
    return Add(input1, input2)[:]

def divide(input1, input2):
    return Divide(input1, input2)[:]

def multiply(input1, input2):
    return Multiply(input1, input2)[:]

def offset(input_, value):
    return Offset(input_, value)[:]

def scale(input_, value):
    return Scale(input_, value)[:]

def subtract(input1, input2):
    return Subtract(input1, input2)[:]
