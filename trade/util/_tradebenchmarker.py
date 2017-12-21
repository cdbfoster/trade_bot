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
        prefix = average_distance // 2
        suffix = average_distance - prefix

        averaged_prices = [np.mean(prices[i - prefix: i + suffix]) for i in range(prefix, len(prices) - suffix + 1)]

        averaged_prices = averaged_prices
        extrema = [0] * len(prices)
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
                    extrema[i + prefix] = 1 if before_sign > 0 else -1

        self.extrema = extrema

        self.benchmark = 100 * (prices[-1] / prices[0] - 1)

        self.maximum = [prices[0], 0]
        self.minimum = [prices[0], 0]

        first_extreme = None
        for e in extrema:
            if e != 0:
                first_extreme = e
                break

        if first_extreme == 1:
            self.maximum = [0, 1]
        elif first_extreme == -1:
            self.minimum = [0, 1]

        for i in range(len(prices)):
            if extrema[i] == 1:
                if self.maximum[1] > 0:
                    self.maximum[0] += prices[i] * self.maximum[1]
                    self.maximum[1] = 0
                if self.minimum[0] > 0:
                    self.minimum[1] += self.minimum[0] / prices[i]
                    self.minimum[0] = 0
            elif extrema[i] == -1:
                if self.maximum[0] > 0:
                    self.maximum[1] += self.maximum[0] / prices[i]
                    self.maximum[0] = 0
                if self.minimum[1] > 0:
                    self.minimum[0] += prices[i] * self.minimum[1]
                    self.minimum[1] = 0

        self.maximum[0] += prices[-1] * self.maximum[1]
        self.minimum[0] += prices[-1] * self.minimum[1]

        self.maximum = 100 * (self.maximum[0] / prices[0] - 1)
        self.minimum = 100 * (self.minimum[0] / prices[0] - 1)
