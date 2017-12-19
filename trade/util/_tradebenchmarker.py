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

import math
import numpy as np

class TradeBenchmarker:
    def __init__(self, prices, average_distance=18):
        prefix = math.floor(average_distance / 2) if average_distance % 2 != 0 else average_distance / 2
        suffix = average_distance - prefix

        averaged_prices = [np.mean(prices[i - prefix: i + suffix]) for i in range(prefix, len(prices) - suffix + 1)]

        self.averaged_prices = averaged_prices
        self.extrema = [0] * len(prices)
        hold = None
        for i in range(1, len(averaged_prices) - 1):
            before = averaged_prices[i] - averaged_prices[i - 1]
            after = averaged_prices[i + 1] - averaged_prices[i]

            if hold is None and before == 0:
                continue
            elif hold is None and after == 0:
                hold = before
            elif hold is not None and after != 0:
                before = hold
                hold = None

            if hold is None:
                before_sign = math.copysign(1, before)
                after_sign = math.copysign(1, after)

                if before_sign != after_sign:
                    self.extrema[i + prefix] = 1 if before_sign > 0 else -1
