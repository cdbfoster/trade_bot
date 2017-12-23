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

from trade.inputsource import HistoricalInputSource
from trade.market import _Market, OrderSide, OrderType

class HistoricalMarket(_Market, HistoricalInputSource):
    def __init__(self, exchange_currency, base_currency, filename, start=None, position=None, reverse=False):
        _Market.__init__(self, exchange_currency, base_currency)
        HistoricalInputSource.__init__(self, filename, start, position, reverse)

    def place_order(self, order_side, order_type, amount, cancel_existing=True):
        exchange_amount = None
        base_amount = None

        if order_side == OrderSide.BUY:
            exchange_amount = amount / self.get_last_price()
            base_amount = amount
        elif order_side == OrderSide.SELL:
            exchange_amount = amount
            base_amount = amount * self.get_last_price()
        else:
            raise ValueError("invalid order side")

        if order_type != OrderType.MARKET:
            raise ValueError("HistoricalMarket only accepts market orders")

        if order_side == OrderSide.BUY and self.balance[self.base_currency] >= base_amount:
            self.balance[self.base_currency] -= base_amount
            self.balance[self.exchange_currency] += exchange_amount
            return True
        elif order_side == OrderSide.SELL and self.balance[self.exchange_currency] >= exchange_amount:
            self.balance[self.exchange_currency] -= exchange_amount
            self.balance[self.base_currency] += base_amount
            return True
        else:
            return False

    def cancel_existing_orders(self):
        pass

    def get_last_price(self):
        return self[-1] if len(self) > 0 else None

    def get_portfolio_value(self):
        return self.get_last_price() * self.balance[self.exchange_currency] + self.balance[self.base_currency]
