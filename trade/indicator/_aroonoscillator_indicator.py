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

from trade.function import AroonOscillatorFunction
from trade.indicator import Indicator, Signal

class AroonOscillatorIndicator(Indicator):
    def __init__(self, input_, period, debug=None):
        self.__input = input_
        self.__period = period
        self.debug = debug

        if debug is not None:
            debug.write("input aroon-oscillator signal\n")

        self.__aroon_oscillator = AroonOscillatorFunction(input_, period=period)
        self.__last_spike = None
        self.__threshold = 1 - 1 / self.__period

    def get_signal(self):
        if len(self.__aroon_oscillator) < 2:
            return None

        ao = self.__aroon_oscillator[-2:]

        if math.copysign(1, ao[-2]) != math.copysign(1, ao[-1]):
            return self.__last_spike if self.__last_spike is not None and self.__last_spike.value == math.copysign(1, ao[-1]) else Signal.HOLD

        return Signal.HOLD

    def update(self, steps=1):
        ao = self.__aroon_oscillator[-steps - 1:]
        input_ = self.__input[-len(ao):] if self.debug is not None and len(ao) > 0 else None

        if len(ao) == 0:
            return

        for i, a in enumerate(ao[1:]):
            i += 1
            if abs(a) >= self.__threshold:
                self.__last_spike = Signal.BUY if a < 0 else Signal.SELL

            if self.debug is not None and len(ao) > steps:
                signal = self.__last_spike if math.copysign(1, ao[i - 1]) != math.copysign(1, ao[i]) and \
                    self.__last_spike is not None and self.__last_spike.value == math.copysign(1, ao[i]) else None
                self.debug.write("{} {} {}\n".format(
                    input_[i],
                    ao[i],
                    signal.value if signal is not None else 0,
                ))
