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

from trade.function import Function
from trade.indicator import Indicator, Signal
from trade.util import buy_down_price, buy_up_price, sell_down_price

class Benchmark(Indicator):
    def __init__(self, trade_loss, transaction_fee, sequence, minimum_return=0):
        self.trade_loss = trade_loss
        self.transaction_fee = transaction_fee
        self.sequence = sequence
        self.minimum_return = minimum_return

        self.__swing = (1 + trade_loss) * (1 + transaction_fee) * (1 + minimum_return) / (1 - trade_loss) / (1 - transaction_fee)

        if len(Function.evaluate_sequence(self, sequence)) == 0:
            return []

        for _, index, signal in self.extrema:
            self._Function__values[index] = signal

    def _first(self, x):
        self.__local_max = (x, 0, Signal.SELL)
        self.__local_min = (x, 0, Signal.BUY)

        self.extrema = []

        return Signal.HOLD

    def _next(self, x):
        index = len(self)

        if x >= self.__local_max[0]:
            self.__local_max = (x, index, Signal.SELL)
        elif x <= self.__local_min[0]:
            self.__local_min = (x, index, Signal.BUY)

        if x < self.__local_max[0] / self.__swing and (len(self.extrema) == 0 or self.extrema[-1] is not self.__local_max):
            self.extrema.append(self.__local_max)
            self.__local_min = (x, index, Signal.BUY)
        elif x > self.__local_min[0] * self.__swing and (len(self.extrema) == 0 or self.extrema[-1] is not self.__local_min):
            self.extrema.append(self.__local_min)
            self.__local_max = (x, index, Signal.SELL)

        return Signal.HOLD

    def evaluate(self, x):
        raise RuntimeError("cannot run evaluate on a Benchmark indicator")

    def evaluate_sequence(self, sequence):
        raise RuntimeError("cannot run evaluate_sequence on a Benchmark indicator")

    def maximum_return(self):
        try:
            return self.__maximum_return
        except AttributeError:
            self.__maximum_return = self.indicator_return(self)
            return self.__maximum_return

    def indicator_return(self, indicator, final_sell=False):
        if len(indicator) == 0:
            indicator.evaluate_sequence(self.sequence)
        elif len(indicator) != len(self):
            raise RuntimeError("indicator has a different length than the benchmark")

        value = 1.0
        bought = None

        for i in range(len(self)):
            signal = indicator[i]
            if signal is Signal.HOLD:
                continue

            price = self.sequence[i]
            if bought is None and signal is Signal.BUY:
                bought = price
                value *= price / buy_up_price(price, self.trade_loss, self.transaction_fee)
            elif bought is not None and signal is Signal.SELL:
                value *= sell_down_price(price, self.trade_loss, self.transaction_fee) / bought
                bought = None
        if bought is not None and final_sell:
            value *= sell_down_price(self.sequence[-1], self.trade_loss, self.transaction_fee) / bought

        return value - 1

    def relative_return(self, indicator):
        return (self.indicator_return(indicator) + 1) / (self.maximum_return() + 1)

    def indicator_similarity(self, indicator):
        if len(indicator) == 0:
            indicator.evaluate_sequence(self.sequence)
        elif len(indicator) != len(self):
            raise RuntimeError("indicator has a different length than the benchmark")

        buys = [x for x in enumerate(indicator) if x[1] is Signal.BUY]
        sells = [x for x in enumerate(indicator) if x[1] is Signal.SELL]

        total_score = 0
        for i, extreme in enumerate(self.extrema):
            count = 0
            score = 0
            start = self.extrema[i - 1][1] if i > 0 else extreme[1]
            end = self.extrema[i + 1][1] if i < len(self.extrema) - 1 else extreme[1]

            for event in (buys if extreme[2] is Signal.BUY else sells):
                if event[0] >= start and event[0] <= end:
                    count += 1
                    score += (1 - abs(extreme[1] - event[0]) / ((extreme[1] - start) if event[0] < extreme[1] else (end - extreme[1]))) if event[0] != extreme[1] else 1

                if event[0] > end:
                    break

            total_score += (score / count) if count > 0 else 0

        return total_score / len(self.extrema)
