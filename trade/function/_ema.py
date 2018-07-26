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

import numpy as np

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
