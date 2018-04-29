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
from trade.util import down_price, return_value, up_price

class SingleIndicator(Investor):
    class _Investment:
        def __init__(self, amount, actual_purchase, price):
            self.amount = amount
            self.actual_purchase = actual_purchase
            self.price = price
            self.max_since = amount

    def __init__(self, market, indicator, maximum_trade=None, trailing_stop_loss=0.15, sim_trade_loss=0.001, sim_transaction_fee=0.0025, maximum_investments=1, debug=None):
        Investor.__init__(self, market)

        self.debug = debug

        self.indicator = indicator
        self.maximum_trade = maximum_trade
        self.trailing_stop_loss = trailing_stop_loss
        self.sim_trade_loss = sim_trade_loss
        self.sim_transaction_fee = sim_transaction_fee
        self.maximum_investments = maximum_investments

        self.investments = []

    def update(self):
        last_price = self.market.get_last_price()
        self.orders.append(Signal.HOLD)

        # Check stop-losses
        for investment in self.investments[:]:
            investment.max_since = max(last_price, investment.max_since)
            if last_price < investment.max_since * (1.0 - self.trailing_stop_loss):
                print("{} is less than {}% below {}.  Stop-loss triggered.".format(last_price, self.trailing_stop_loss * 100, investment.max_since))
                self.market.place_order(OrderSide.SELL, OrderType.MARKET, investment.actual_purchase)
                self.investments.remove(investment)
                self.orders[-1] = Signal.SELL

        signal = None
        try:
            signal = self.indicator[-1]
        except ValueError:
            return

        if signal == Signal.HOLD:
            return

        if signal == Signal.BUY and self.market.balance[self.market.base_currency] > 0 and len(self.investments) < self.maximum_investments:
            buy_allowed = True
            for investment in self.investments:
                top = down_price(max(last_price, investment.price), self.sim_trade_loss, self.sim_transaction_fee)
                bottom = up_price(min(last_price, investment.price), self.sim_trade_loss, self.sim_transaction_fee)

                if top <= bottom:
                    buy_allowed = False
                    break

            if buy_allowed:
                amount = self.market.balance[self.market.base_currency] / (self.maximum_investments - len(self.investments))
                if self.maximum_trade is not None:
                    amount = min(amount, self.maximum_trade * last_price)

                old_balance = self.market.balance.copy()
                old_value = self.market.get_portfolio_value()
                self.market.place_order(OrderSide.BUY, OrderType.MARKET, amount)
                self.investments.append(SingleIndicator._Investment(
                    amount,
                    self.market.balance[self.market.exchange_currency] - old_balance[self.market.exchange_currency],
                    last_price,
                ))
                self.orders[-1] = Signal.BUY

                if self.debug is not None:
                    self.debug.write("BUY - Price: {:.2f}, Before: {}, Value: {:.2f}, After: {}, Value: {:.2f}\n".format(last_price, old_balance, old_value, self.market.balance, self.market.get_portfolio_value()))

        if signal == Signal.SELL and self.market.balance[self.market.exchange_currency] > 0 and len(self.investments) > 0:
            max_return = max([(return_value(last_price, self.sim_trade_loss, self.sim_transaction_fee, investment.amount / investment.actual_purchase), investment) for investment in self.investments])

            if max_return[0] > 0:
                self.investments.remove(max_return[1])
                old_balance = self.market.balance.copy()
                old_value = self.market.get_portfolio_value()
                self.market.place_order(OrderSide.SELL, OrderType.MARKET, max_return[1].actual_purchase)
                self.orders[-1] = Signal.SELL

                if self.debug is not None:
                    self.debug.write("SELL - Price: {:.2f}, Before: {}, Value: {:.2f}, After: {}, Value: {:.2f}\n".format(last_price, old_balance, old_value, self.market.balance, self.market.get_portfolio_value()))
