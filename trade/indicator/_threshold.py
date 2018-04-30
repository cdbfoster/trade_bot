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

from trade.indicator import Indicator, Signal

class Threshold(Indicator):
    def __init__(self, input_, threshold, signal, fuzziness=None):
        self.input = input_
        self.__threshold = threshold
        self.__signal = signal
        self.__fuzziness = fuzziness

        Indicator.__init__(self)

    def _next(self):
        self.input._update()

        if len(self) == len(self.input):
            raise StopIteration

        this_value = self.input[len(self)]

        if this_value >= self.__threshold - (self.__fuzziness if self.__fuzziness is not None else 0):
            self._values.append(self.__signal)
        else:
            self._values.append(Signal.HOLD)
