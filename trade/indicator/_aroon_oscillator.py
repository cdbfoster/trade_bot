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

from trade.function import AroonOscillator as AroonOscillatorFunction, PeriodAdjustedAroonOscillator as PeriodAdjustedAroonOscillatorFunction
from trade.indicator import Indicator, Signal

class AroonOscillator(Indicator):
    def __init__(self, input_, period):
        self.input = input_
        self.__period = period

        self.__aroon_oscillator = AroonOscillatorFunction(self.input, self.__period)
        self.__last_spike = None

        Indicator.__init__(self)

    def _next(self):
        self.__aroon_oscillator._update()

        if len(self.__aroon_oscillator) < 2 or len(self) == len(self.__aroon_oscillator) - 1:
            raise StopIteration

        last_aro = self.__aroon_oscillator[len(self)]
        this_aro = self.__aroon_oscillator[len(self) + 1]

        if abs(last_aro) > 99.9:
            self.__last_spike = Signal.SELL if math.copysign(1, last_aro) > 0 else Signal.BUY

        if math.copysign(1, last_aro) != math.copysign(1, this_aro) and self.__last_spike is not None:
            self._values.append(self.__last_spike if self.__last_spike.value == math.copysign(1, this_aro) else Signal.HOLD)
        else:
            self._values.append(Signal.HOLD)

class PeriodAdjustedAroonOscillator(Indicator):
    def __init__(self, input_, period_function, max_period):
        self.input = input_
        self.__period = period_function
        self.__max_period = max_period

        self.__aroon_oscillator = PeriodAdjustedAroonOscillatorFunction(self.input, self.__period, self.__max_period)
        self.__last_spike = None

        Indicator.__init__(self)

    def _next(self):
        self.__aroon_oscillator._update()

        if len(self.__aroon_oscillator) < 2 or len(self) == len(self.__aroon_oscillator) - 1:
            raise StopIteration

        last_aro = self.__aroon_oscillator[len(self)]
        this_aro = self.__aroon_oscillator[len(self) + 1]

        if abs(last_aro) > 99.9:
            self.__last_spike = Signal.SELL if math.copysign(1, last_aro) > 0 else Signal.BUY
            self._values.append(self.__last_spike)
        elif math.copysign(1, last_aro) != math.copysign(1, this_aro):
            if self.__last_spike is None:
                self._values.append(Signal.SELL if math.copysign(1, last_aro) > 0 else Signal.BUY)
            else:
                self.__last_spike = None
                self._values.append(Signal.HOLD)
        else:
            self._values.append(Signal.HOLD)
