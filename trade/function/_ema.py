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

class Ema(Function):
    def __init__(self, period):
        self.period = period

        self.__weight = 2 / (period + 1)

    def _first(self, x):
        self.__last_value = x
        return x

    def _next(self, x):
        self.__last_value = self.__weight * x + (1 - self.__weight) * self.__last_value
        return self.__last_value

class EmaDifference(Function):
    def __init__(self, period_a, period_b):
        self.period_a = period_a
        self.period_b = period_b

        self.__ema_a = Ema(period_a)
        self.__ema_b = Ema(period_b)

    def _first(self, x):
        return self.__ema_a._first(x) - self.__ema_b._first(x)

    def _next(self, x):
        return self.__ema_a._next(x) - self.__ema_b._next(x)
