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

        self.__values = []
        self.__initialize()

    def __getitem__(self, index):
        return self.__values[index]

    def __len__(self):
        return len(self.__values)

    def update(self, steps=1, update_input=True):
        if update_input:
            self.input.update(steps)

        if len(self.__values) == 0:
            self.__initialize()
        else:
            for i in range(-steps, 0):
                self.__values.append(self.input[i] - self.input[i - 1])

    def __initialize(self):
        if len(self.input) < 2:
            return

        for i in range(len(self.input) - 1):
            self.__values.append(self.input[i + 1] - self.input[i])
