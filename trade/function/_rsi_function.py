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

from trade.function import _Function, DifferenceFunction

class RsiFunction(_Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.__difference = DifferenceFunction(input_)

    def __len__(self):
        return max(len(self.__difference) - 2 * self.__period + 1, 0)

    def _calculate_values(self, count):
        count = min(count, len(self))
        if count <= 0:
            return []

        difference = self.__difference[:2 * self.__period + count - 1]

        average_gain = np.mean([max(difference[i], 0) for i in range(self.__period)])
        average_loss = np.mean([min(difference[i], 0) for i in range(self.__period)])

        for i in range(self.__period, 2 * self.__period - 1):
            average_gain = (average_gain * (self.__period - 1) + max(difference[i], 0)) / self.__period
            average_loss = (average_loss * (self.__period - 1) + min(difference[i], 0)) / self.__period

        values = []
        for i in range(2 * self.__period - 1, 2 * self.__period + count - 1):
            average_gain = (average_gain * (self.__period - 1) + max(difference[i], 0)) / self.__period
            average_loss = (average_loss * (self.__period - 1) + min(difference[i], 0)) / self.__period
            values.append(100 - 100 / (1 + average_gain / abs(average_loss)))

        return values
