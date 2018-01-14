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

from trade.function import Function, EmaFunction

class MacdFunction(Function):
    def __init__(self, input_, short_period, long_period):
        if short_period >= long_period:
            raise ValueError("short_period must be less than long_period")

        self.input = input_

        self.__short = EmaFunction(input_, period=short_period)
        self.__long = EmaFunction(input_, period=long_period)

        Function.__init__(self)

    def _first(self):
        self._next()

    def _next(self):
        self.__short._exhaust_input()
        self.__long._exhaust_input()

        if len(self.__long) == 0 or len(self) == len(self.__long):
            raise StopIteration

        offset = len(self.__short) - len(self.__long)
        self._values.append(self.__short[len(self) + offset] - self.__long[len(self)])
