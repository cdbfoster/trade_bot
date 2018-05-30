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

from trade.function import EhlersWayBandpass, Function, FunctionInput, StandardDeviation

class DominantBand(Function):
    def __init__(self, input_, std_dev_period, band_min, band_max, band_count, interpolate):
        self.__input = FunctionInput(input_)
        self.__interpolate = interpolate

        self.__band_periods = np.geomspace(band_min, band_max, band_count)
        self.__bands = list(FunctionInput(StandardDeviation(EhlersWayBandpass(input_, period, 0.5), std_dev_period)) for period in self.__band_periods)
        for i, band in enumerate(self.__bands):
            setattr(self, "_DominantBand__band{}".format(i), band)

        Function.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.__bands[0]):
            raise StopIteration

        self.inputs.sync_to_min_length()

        self.__input.consume()
        std_devs = [band.consume() for band in self.__bands]

        value = 0
        if self.__interpolate:
            value = 1
            normalized_std_devs = np.array(std_devs) / np.sum(std_devs)
            for i in range(0, len(self.__bands)):
                value *= self.__band_periods[i] ** normalized_std_devs[i]
        else:
            value = self.__band_periods[np.argmax(std_devs)]

        self._values.append(value)
