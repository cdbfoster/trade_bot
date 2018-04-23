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

class And(Indicator):
    def __init__(self, input1, input2):
        self.input = input1
        self.input1 = input1
        self.input2 = input2

        Indicator.__init__(self)

    def _next(self):
        self.input1._update()
        self.input2._update()

        input1_shift = max(len(self.input1) - len(self.input2), 0)
        input2_shift = max(len(self.input2) - len(self.input1), 0)

        input_index = len(self)
        if input_index + input1_shift >= len(self.input1) or input_index + input2_shift >= len(self.input2):
            raise StopIteration

        signal = self.input1[input_index + input1_shift]
        if signal != self.input2[input_index + input2_shift]:
            signal = Signal.HOLD

        self._values.append(signal)

class Not(Indicator):
    def __init__(self, input_):
        self.input = input_

        Indicator.__init__(self)

    def _next(self):
        self.input._update()

        input_index = len(self)
        if input_index >= len(self.input):
            raise StopIteration

        signal = Signal.HOLD
        if self.input[input_index] is Signal.BUY:
            signal = Signal.SELL
        elif self.input[input_index] is Signal.SELL:
            signal = Signal.BUY

        self._values.append(signal)

class Or(Indicator):
    def __init__(self, input1, input2):
        self.input = input1
        self.input1 = input1
        self.input2 = input2

        Indicator.__init__(self)

    def _next(self):
        self.input1._update()
        self.input2._update()

        input1_shift = max(len(self.input1) - len(self.input2), 0)
        input2_shift = max(len(self.input2) - len(self.input1), 0)

        input_index = len(self)
        if input_index + input1_shift >= len(self.input1) or input_index + input2_shift >= len(self.input2):
            raise StopIteration

        signal = self.input1[input_index + input1_shift]
        if signal == Signal.HOLD:
            signal = self.input2[input_index + input2_shift]

        self._values.append(signal)
