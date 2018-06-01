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

class And(Indicator):
    def __init__(self, input1, input2):
        self.__input1 = IndicatorInput(input1)
        self.__input2 = IndicatorInput(input2)

        Indicator.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= min(len(self.__input1), len(self.__input2)):
            raise StopIteration

        self.inputs.sync()

        input1 = self.__input1.consume()
        input2 = self.__input2.consume()

        signal = input1
        if signal != input2:
            signal = Signal.HOLD

        self._values.append(signal)

class Not(Indicator):
    def __init__(self, input_):
        self.__input = IndicatorInput(input_)

        Indicator.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= len(self.__input):
            raise StopIteration

        input_ = self.__input.consume()

        signal = Signal.HOLD
        if input_ is Signal.BUY:
            signal = Signal.SELL
        elif input_ is Signal.SELL:
            signal = Signal.BUY

        self._values.append(signal)

class Or(Indicator):
    def __init__(self, input1, input2):
        self.__input1 = IndicatorInput(input1)
        self.__input2 = IndicatorInput(input2)

        Indicator.__init__(self)

    def _next(self):
        self.inputs.update()

        if len(self) >= min(len(self.__input1), len(self.__input2)):
            raise StopIteration

        self.inputs.sync()

        input1 = self.__input1.consume()
        input2 = self.__input2.consume()

        signal = input1
        if signal == Signal.HOLD:
            signal = input2

        self._values.append(signal)
