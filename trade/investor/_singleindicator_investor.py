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

from trade.indicator import Signal
from trade.investor import _Investor
from trade.market import OrderSide, OrderType

class SingleIndicatorInvestor(_Investor):
    def __init__(self, market, indicator, trade_percent=1.0, maximum_trade=None, exchange_amount=None, base_amount=None):
        _Investor.__init__(self, market, exchange_amount, base_amount)

        self.indicator = indicator
        self.trade_percent = trade_percent
        self.maximum_trade = maximum_trade
        self.position = 0

    def tick(self):
        signal = self.indicator.get_signal()

        if signal is None or signal == Signal.HOLD:
            return

        if signal == Signal.SELL and self.market.balance[self.market.exchange_currency] > 0:
            amount = self.market.balance[self.market.exchange_currency] * self.trade_percent
            if self.maximum_trade is not None:
                amount = min(amount, self.maximum_trade)
            self.market.place_order(OrderSide.SELL, OrderType.MARKET, amount)
            self.position -= 1
        elif signal == Signal.BUY and self.market.balance[self.market.base_currency] > 0:
            amount = self.market.balance[self.market.base_currency] * self.trade_percent
            if self.maximum_trade is not None:
                maximum = self.market.get_last_price() * self.maximum_trade
                amount = min(amount, maximum)
            self.market.place_order(OrderSide.BUY, OrderType.MARKET, amount)
            self.position += 1
