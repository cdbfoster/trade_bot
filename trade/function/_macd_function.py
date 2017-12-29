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

        self.input = input_

        self.__short = EmaFunction(input_, period=short_period)
        self.__long = EmaFunction(input_, period=long_period)

    def __len__(self):
        return len(self.__long)

    def _calculate_values(self, count):
        count = min(count, len(self))
        if count <= 0:
            return []

        start = -len(self)
        short = self.__short[start:start + count if start + count < 0 else None]
        long_ = self.__long[start:start + count if start + count < 0 else None]

        return list(s - l for s, l in zip(short, long_))
