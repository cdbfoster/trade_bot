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

from trade.indicator import Indicator, IndicatorInput, Signal

class Threshold(Indicator):
    def __init__(self, input_, threshold, signal, fuzziness=None):
        self.__input = IndicatorInput(input_)
        self.__threshold = IndicatorInput(threshold)
        self.__signal = signal
        self.__fuzziness = IndicatorInput(fuzziness if fuzziness is not None else 0)

        Indicator.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= min(len(self.__input), len(self.__threshold), len(self.__fuzziness)):
            raise StopIteration

        self.inputs.sync()

        this_value = self.__input.consume()
        threshold = self.__threshold.consume()
        fuzziness = self.__fuzziness.consume()

        if this_value >= threshold - fuzziness:
            self._values.append(self.__signal)
        else:
            self._values.append(Signal.HOLD)
