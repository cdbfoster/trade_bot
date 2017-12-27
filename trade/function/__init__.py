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

class _Function:
    def __getitem__(self, index):
        pass

    def __len__(self):
        pass

    def update(self, steps=1):
        pass

    def save(self, filename, mode='w'):
        f = open(filename, mode)
        for x in self:
            f.write("{}\n".format(x))
        f.close()

    def __iter__(self):
        return _Function.__Iter(self)

    class __Iter:
        def __init__(self, function):
            self.function = function
            self.position = 0

        def __next__(self):
            if self.position < len(self.function):
                self.position += 1
                return self.function[self.position - 1]
            raise StopIteration

from ._historicalinput_function import HistoricalInputFunction
