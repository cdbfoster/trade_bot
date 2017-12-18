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

from enum import Enum as _Enum
from enum import auto as _auto

class Signal(_Enum):
    BUY = _auto()
    HOLD = _auto()
    SELL = _auto()

class _Indicator:
    def get_signal(self):
        pass

    def update(self, steps=1):
        pass

from ._emacrossover_indicator import EMACrossoverIndicator
