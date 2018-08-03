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

class Rsi(Function):
    def __init__(self, period):
        self.period = period

    def _first(self, x):
        self.__last_input = x
        self.__average_gain = 0
        self.__average_loss = 0

        return 50

    def _next(self, x):
        dx = x - self.__last_input

        self.__last_input = x
        self.__average_gain = (self.__average_gain * (self.period - 1) + max(dx, 0)) / self.period
        self.__average_loss = (self.__average_loss * (self.period - 1) + min(dx, 0)) / self.period

        if self.__average_loss != 0:
            return 100 - 100 / (1 + self.__average_gain / -self.__average_loss))
        else:
            return 100
