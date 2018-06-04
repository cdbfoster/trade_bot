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

class Lerp(Function):
    def __init__(self, input1, input2, x):
        self.input1 = FunctionInput(input1)
        self.input2 = FunctionInput(input2)
        self.x = FunctionInput(x)

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= min(len(self.input1), len(self.input2), len(self.x)):
            raise StopIteration

        self.inputs.sync()

        a = self.input1.consume()
        b = self.input2.consume()
        x = self.x.consume()

        self._values.append(a * (1 - x) + b * x)
