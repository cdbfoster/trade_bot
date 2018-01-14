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

class DifferenceFunction(_Function):
    def __init__(self, input_):
        self.input = input_

        _Function.__init__(self)

    def _first(self):
        self._next()

    def _next(self):
        input_index = len(self) + 1
        if input_index >= len(self.input):
            raise StopIteration

        self._values.append(self.input[input_index] - self.input[input_index - 1])
