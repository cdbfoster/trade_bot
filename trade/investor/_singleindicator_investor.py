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

from trade.indicator import Signal as _Signal
from trade.investor import _Investor

class SingleIndicatorInvestor(_Investor):
    def __init__(self, market, exchange_amount, base_amount, indicator, trade_percent):
        _Investor.__init__(self, market, exchange_amount, base_amount)

        self.indicator = indicator
        self.trade_percent = trade_percent
        self.position = 0

    def tick(self):
        signal = self.indicator.get_signal()

        if signal is None or signal == _Signal.HOLD:
            return

        if signal == _Signal.SELL and (self.position == 1 or (self.position == 0 and self.market.balance[self.market.exchange_currency] > 0)):
            amount = self.market.balance[self.market.exchange_currency] * self.trade_percent
            print("Selling {} BTC".format(amount))
            self.market.sell(self.market.exchange_currency, amount)
            self.position = -1
        elif signal == _Signal.BUY and (self.position == -1 or (self.position == 0 and self.market.balance[self.market.base_currency] > 0)):
            amount = self.market.balance[self.market.base_currency] * self.trade_percent
            print("Buying {} USD worth of BTC".format(amount))
            self.market.sell(self.market.base_currency, amount)
            self.position = 1
