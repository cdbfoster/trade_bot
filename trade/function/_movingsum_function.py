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

from trade.function import _Function

class MovingSumFunction(_Function):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

    def __len__(self):
        return max(len(self.input) - self.__period + 1, 0)

    def _calculate_values(self, count):
        count = min(count, len(self))
        if count <= 0:
            return []

        input_ = self.input[:self.__period + count - 1]

        ms = np.sum(input_[:self.__period])

        values = [ms]
        for i in range(self.__period, self.__period + count - 1):
            ms -= input_[i - self.__period]
            ms += input_[i]
            values.append(ms)

        return values
