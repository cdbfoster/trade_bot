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

from trade.function import _Function, EmaFunction

class MacdFunction(_Function):
    def __init__(self, input_, short_period, long_period):
        if short_period >= long_period:
            raise ValueError("short_period must be less than long_period")

        self.__input = input_

        self.__short = EmaFunction(input_, period=short_period)
        self.__long = EmaFunction(input_, period=long_period)

        self.__values = []
        self.__initialize()

    def __getitem__(self, index):
        return self.__values[index]

    def __len__(self):
        return len(self.__values)

    def update(self, steps=1, update_input=True):
        if update_input:
            self.__input.update(steps)

        self.__short.update(steps, update_input=False)
        self.__long.update(steps, update_input=False)

        if len(self.__values) == 0:
            self.__initialize()
        else:
            for i in range(-steps, 0):
                self.__values.append(self.__short[i] - self.__long[i])

    def __initialize(self):
        if len(self.__long) == 0:
            return

        for i in range(-len(self.__long), 0):
            self.__values.append(self.__short[i] - self.__long[i])
