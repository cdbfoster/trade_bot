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

class ChangePeriod(Function):
    def __init__(self, input_, change, sample_range):
        self.input = input_
        self.__change = change
        self.__range = sample_range

        Function.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self) + self.__range
        if input_index > len(self.input):
            raise StopIteration

        frequencies = np.fft.rfftfreq(self.__range)[::-1]

        samples = np.array(self.input[input_index - self.__range:input_index])
        min_ = np.min(samples)
        range_ = np.max(samples) - min_

        fourier_transform = np.fft.rfft(2 * (samples - min_) / range_ - 1) / (0.5 * self.__range)

        magnitude = np.abs(fourier_transform)[::-1]

        target_magnitude = np.mean(samples) * abs(0.5 * self.__change) / range_

        if target_magnitude <= np.max(magnitude):
            if target_magnitude > magnitude[0]:
                for i, m in enumerate(magnitude):
                    if m >= target_magnitude:
                        x = (m - target_magnitude) / (m - magnitude[i - 1])
                        frequency = frequencies[i - 1] * x + frequencies[i] * (1 - x)
                        self._values.append(min(1 / frequency, self.__range))
                        break
            else:
                self._values.append(1 / frequencies[0])
        else:
            self._values.append(self.__range)

def change_period(input_, change, sample_range):
    return ChangePeriod(input_, change, sample_range)[:]
