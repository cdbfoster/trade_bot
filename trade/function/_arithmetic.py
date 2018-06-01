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

class Add(Function):
    def __init__(self, input1, input2):
        self.input1 = FunctionInput(input1)
        self.input2 = FunctionInput(input2)

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.input1) or len(self) >= len(self.input2):
            raise StopIteration

        self.inputs.sync()

        a = self.input1.consume()
        b = self.input2.consume()

        self._values.append(a + b)

class Divide(Function):
    def __init__(self, input1, input2):
        self.input1 = FunctionInput(input1)
        self.input2 = FunctionInput(input2)

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.input1) or len(self) >= len(self.input2):
            raise StopIteration

        self.inputs.sync()

        a = self.input1.consume()
        b = self.input2.consume()

        b = b if b != 0 else 0.00000001

        self._values.append(a / b)

class Multiply(Function):
    def __init__(self, input1, input2):
        self.input1 = FunctionInput(input1)
        self.input2 = FunctionInput(input2)

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.input1) or len(self) >= len(self.input2):
            raise StopIteration

        self.inputs.sync()

        a = self.input1.consume()
        b = self.input2.consume()

        self._values.append(a * b)

class Subtract(Function):
    def __init__(self, input1, input2):
        self.input1 = FunctionInput(input1)
        self.input2 = FunctionInput(input2)

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.input1) or len(self) >= len(self.input2):
            raise StopIteration

        self.inputs.sync()

        a = self.input1.consume()
        b = self.input2.consume()

        self._values.append(a - b)
