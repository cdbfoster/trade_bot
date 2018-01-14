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

class HistoricalInput(Function):
    def __init__(self, filename, start=None, position=None, reverse=False):
        self.__prices = list(float(line.strip()) for line in open(filename))

        if reverse:
            self.__prices = self.__prices[::-1]
        if start:
            self.__prices = self.__prices[start:]

        self.__position = position if position is not None else max(len(self.__prices) - 1, 0)

        Function.__init__(self)

    def _first(self):
        self._next()

    def _next(self):
        if len(self) > self.__position or len(self.__prices) == 0:
            raise StopIteration

        self._values.append(self.__prices[len(self)])

    def update(self, steps=1):
        self.__position = max(min(self.__position + steps, len(self.__prices) - 1), 0)

        for _ in range(steps):
            try:
                self._next()
            except StopIteration:
                break

    def remaining(self):
        return max(len(self.__prices) - self.__position - 1, 0)

def historical_input(filename):
    return HistoricalInput(filename)[:]
