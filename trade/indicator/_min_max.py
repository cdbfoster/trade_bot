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

class MinMax(Indicator):
    def __init__(self, input_, min_value, max_value, fuzziness=None, continuous=False):
        self.__input = IndicatorInput(input_)
        self.__min = IndicatorInput(min_value)
        self.__max = IndicatorInput(max_value)
        self.__fuzziness = IndicatorInput(fuzziness if fuzziness is not None else 0)
        self.__continuous = continuous

        Indicator.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= min(len(self.__input), len(self.__min), len(self.__max), len(self.__fuzziness)):
            raise StopIteration

        self.inputs.sync()

        this_value = self.__input.consume()
        min_ = self.__min.consume()
        max_ = self.__max.consume()
        fuzziness = self.__fuzziness.consume()

        if this_value >= max_ - fuzziness and (self.__continuous or len(self) == 0 or self._values[-1] is not Signal.SELL):
            self._values.append(Signal.SELL)
        elif this_value <= min_ + fuzziness and (self.__continuous or len(self) == 0 or self._values[-1] is not Signal.BUY):
            self._values.append(Signal.BUY)
        else:
            self._values.append(Signal.HOLD)
