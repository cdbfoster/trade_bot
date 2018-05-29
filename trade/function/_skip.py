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

class Skip(Function):
    def __init__(self, input_, skip):
        self.__input = FunctionInput(input_)
        self.__skip = int(skip)

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) + self.__skip > len(self.__input):
            raise StopIteration

        self.inputs.sync_to_input_index(self.__input, self.__skip)

        self._values.append(self.__input.consume())
