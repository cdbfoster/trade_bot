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

from trade.function import HistoricalInput
from trade.market import Market, OrderSide, OrderType
# XXX from trade.util import down_price, up_price

class HistoricalMarket(Market, HistoricalInput):
    def __init__(self, exchange_currency, base_currency, filename, trade_loss=0.001, transaction_fee=0.0025, start=None, position=None, reverse=False):
        Market.__init__(self, exchange_currency, base_currency)
        HistoricalInput.__init__(self, filename, start, position, reverse)

        self.__trade_loss = trade_loss
        self.__transaction_fee = transaction_fee

    def place_order(self, order_side, order_type, amount, cancel_existing=True):
        exchange_amount = None
        base_amount = None

        if order_side == OrderSide.BUY:
            exchange_amount = amount / up_price(self.get_last_price(), self.__trade_loss, self.__transaction_fee)
            base_amount = amount
        elif order_side == OrderSide.SELL:
            exchange_amount = amount
            base_amount = amount * down_price(self.get_last_price(), self.__trade_loss, self.__transaction_fee)
        else:
            raise ValueError("invalid order side")

        if order_type != OrderType.MARKET:
            raise ValueError("HistoricalMarket only accepts market orders")

        if order_side == OrderSide.BUY and self.balance[self.base_currency] >= base_amount:
            self.balance[self.base_currency] -= base_amount
            self.balance[self.exchange_currency] += exchange_amount
            print("{} - Price: {:.2f}, Value: {}".format(order_side.name, self.get_last_price(), self.get_portfolio_value()))
            return True
        elif order_side == OrderSide.SELL and self.balance[self.exchange_currency] >= exchange_amount:
            self.balance[self.exchange_currency] -= exchange_amount
            self.balance[self.base_currency] += base_amount
            print("{} - Price: {:.2f}, Value: {}".format(order_side.name, self.get_last_price(), self.get_portfolio_value()))
            return True
        else:
            return False

    def cancel_existing_orders(self):
        pass

    def get_last_price(self):
        return self[-1] if len(self) > 0 else None
