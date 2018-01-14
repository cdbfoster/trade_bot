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
from trade.investor import Investor
from trade.market import OrderSide, OrderType

class SingleIndicatorInvestor(Investor):
    def __init__(self, market, indicator, maximum_trade=None, sim_trade_loss=0.001, sim_transaction_fee=0.0025, maximum_campaigns=1, exchange_amount=None, base_amount=None, debug=None):
        Investor.__init__(self, market, exchange_amount, base_amount)

        self.debug = debug

        self.indicator = indicator
        self.maximum_trade = maximum_trade
        self.sim_trade_loss = sim_trade_loss
        self.sim_transaction_fee = sim_transaction_fee
        self.maximum_campaigns = maximum_campaigns

        self.last_signal = None
        self.last_action_price = None
        self.campaigns = []

    def tick(self):
        signal = self.indicator.get_signal()

        if signal is None or signal == Signal.HOLD:
            return

        last_price = self.market.get_last_price()

        if signal == Signal.SELL and self.market.balance[self.market.exchange_currency] > 0 and len(self.campaigns) > 0:
            changes = [last_price * actual * (1 - self.sim_trade_loss) * (1 - self.sim_transaction_fee) - investment for investment, actual, _ in self.campaigns]
            max_ = None
            for i, change in enumerate(changes):
                if max_ is not None and change > max_[1] or max_ is None:
                    max_ = (i, change)

            if max_[1] > 0 or len(self.campaigns) == self.maximum_campaigns:
                campaign = self.campaigns.pop(max_[0])
                old_balance = self.market.balance.copy()
                old_value = self.market.get_portfolio_value()
                self.market.place_order(OrderSide.SELL, OrderType.MARKET, campaign[1])

                self.last_action_price = last_price

                if self.debug is not None:
                    self.debug.write("SELL - Price: {:.2f}, Before: {}, Value: {:.2f}, After: {}, Value: {:.2f}\n".format(last_price, old_balance, old_value, self.market.balance, self.market.get_portfolio_value()))

        elif signal == Signal.BUY and self.market.balance[self.market.base_currency] > 0 and len(self.campaigns) < self.maximum_campaigns:
            top = max(last_price, self.last_action_price)  * (1 - self.sim_trade_loss) * (1 - self.sim_transaction_fee) if self.last_action_price is not None else None
            bottom = min(last_price, self.last_action_price) * (1 + self.sim_trade_loss) / (1 - self.sim_transaction_fee) if self.last_action_price is not None else None

            buy_allowed = top > bottom if self.last_action_price else True

            if buy_allowed:
                for campaign in self.campaigns:
                    top = max(last_price, campaign[2])  * (1 - self.sim_trade_loss) * (1 - self.sim_transaction_fee)
                    bottom = min(last_price, campaign[2]) * (1 + self.sim_trade_loss) / (1 - self.sim_transaction_fee)

                    if top <= bottom:
                        buy_allowed = False
                        break

            if buy_allowed:
                investment = self.market.balance[self.market.base_currency] / (self.maximum_campaigns - len(self.campaigns))
                if self.maximum_trade is not None:
                    investment = min(investment, self.maximum_trade * last_price)

                old_balance = self.market.balance.copy()
                old_value = self.market.get_portfolio_value()
                self.market.place_order(OrderSide.BUY, OrderType.MARKET, investment)
                self.campaigns.append((investment, self.market.balance[self.market.exchange_currency] - old_balance[self.market.exchange_currency], last_price))

                self.last_action_price = last_price

                if self.debug is not None:
                    self.debug.write("BUY - Price: {:.2f}, Before: {}, Value: {:.2f}, After: {}, Value: {:.2f}\n".format(last_price, old_balance, old_value, self.market.balance, self.market.get_portfolio_value()))

        self.last_signal = signal
