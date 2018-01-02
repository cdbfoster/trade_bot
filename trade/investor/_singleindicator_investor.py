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
    def __init__(self, market, indicator, maximum_trade=None, disable=0.0125, maximum_campaigns=1, exchange_amount=None, base_amount=None):
        _Investor.__init__(self, market, exchange_amount, base_amount)

        self.indicator = indicator
        self.maximum_trade = maximum_trade
        self.disable = disable
        self.maximum_campaigns = maximum_campaigns
        self.last_signal = None
        self.campaigns = []

    def tick(self):
        signal = self.indicator.get_signal()

        if signal is None or signal == Signal.HOLD:
            return

        if signal == Signal.SELL and self.market.balance[self.market.exchange_currency] > 0 and len(self.campaigns) > 0:
            last_price = self.market.get_last_price()

            changes = [last_price * investment * (1 - self.disable) - price * investment for price, investment in self.campaigns]
            max_ = None
            for i, change in enumerate(changes):
                if max_ is not None and change > max_[1] or max_ is None:
                    max_ = (i, change)

            if max_[1] > 0 or len(self.campaigns) == self.maximum_campaigns:
                campaign = self.campaigns.pop(max_[0])
                self.market.place_order(OrderSide.SELL, OrderType.MARKET, campaign[1])

        elif signal == Signal.BUY and self.market.balance[self.market.base_currency] > 0 and len(self.campaigns) < self.maximum_campaigns:
            if self.last_signal != Signal.BUY:
                last_price = self.market.get_last_price()
                investment = self.market.balance[self.market.base_currency] / (self.maximum_campaigns - len(self.campaigns))
                if self.maximum_trade is not None:
                    investment = min(investment, self.maximum_trade * last_price)

                old_amount = self.market.balance[self.market.exchange_currency]
                self.market.place_order(OrderSide.BUY, OrderType.MARKET, investment)
                self.campaigns.append((last_price, self.market.balance[self.market.exchange_currency] - old_amount))

        self.last_signal = signal
