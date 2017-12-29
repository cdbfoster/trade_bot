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

    def __len__(self):
        return max(len(self.input) - 1, 0)

    def _calculate_values(self, count):
        count = min(count, len(self))
        if count <= 0:
            return []

        input_ = self.input[:count + 1]

        return list(input_[i + 1] - input_[i] for i in range(count))
