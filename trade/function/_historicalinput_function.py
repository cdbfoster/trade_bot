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

class HistoricalInputFunction(_Function):
    def __init__(self, filename, start=None, position=None, reverse=False):
        self.__prices = list(float(line.strip()) for line in open(filename))
        if reverse:
            self.__prices = self.__prices[::-1]

        self.start = 0

        if start is not None:
            self.start = start if start >= 0 else len(self.__prices) + start

        self.position = len(self.__prices) - self.start

        if position is not None:
            self.position = self.__actual_position(position)

    def __getitem__(self, index):
        if isinstance(index, int):
            position = self.__actual_position(index)
            if position >= self.position or position < 0:
                raise IndexError
            return self.__prices[position + self.start]
        elif isinstance(index, slice):
            start = min(max(self.__actual_position(index.start) if index.start is not None else 0, 0), self.position - 1) + self.start
            stop = min(max(self.__actual_position(index.stop) if index.stop is not None else self.position, 0), self.position) + self.start
            step = index.step
            return self.__prices[start:stop:step]
        else:
            raise TypeError

    def __len__(self):
        return self.position

    def update(self, steps=1):
        self.position = None if self.position is None else self.position + 1

    def total_len(self):
        return len(self.__prices)

    def remaining(self):
        return self.total_len() - len(self) - self.start

    def __actual_position(self, position):
        if position >= 0:
            return position
        else:
            return self.position + position
