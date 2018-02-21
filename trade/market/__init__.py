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

from enum import auto, Enum

class OrderSide(Enum):
    BUY = auto()
    SELL = auto()

class OrderType(Enum):
    LIMIT = auto()
    IMMEDIATE = auto()
    MARKET = auto()

class Market:
    def __init__(self, exchange_currency, base_currency):
        self.exchange_currency = exchange_currency
        self.base_currency = base_currency

        self.currencies = (exchange_currency, base_currency)

        self.balance = {
            exchange_currency: 0.0,
            base_currency: 0.0,
        }

        self.balance_history = {
            exchange_currency: [],
            base_currency: [],
            exchange_currency + "_total": [],
            base_currency + "_total": [],
        }

    def record_balance(self):
        last_price = self.get_last_price()
        exchange = self.balance[self.exchange_currency]
        base = self.balance[self.base_currency]

        self.balance_history[self.exchange_currency].append(exchange)
        self.balance_history[self.base_currency].append(base)
        self.balance_history[self.exchange_currency + "_total"].append(exchange + base / last_price)
        self.balance_history[self.base_currency + "_total"].append(base + exchange * last_price)

    def place_order(self, order_side, order_type, amount, cancel_existing=True):
        pass

    def cancel_active_orders(self):
        pass

    def get_last_price(self):
        pass

    def get_portfolio_value(self):
        return self.get_last_price() * self.balance[self.exchange_currency] + self.balance[self.base_currency]

    def get_orders(self, side):
        pass

    def get_orders_by_count(self, side, count):
        orders = self.get_orders(side)
        return orders[:count] if orders is not None else None

    def get_orders_by_volume(self, side, volume):
        orders = self.get_orders(side)
        if orders is not None:
            current_volume = 0
            for i in range(len(orders)):
                current_volume += orders[i][1]
                if current_volume >= volume:
                    return orders[:i + 1]
        return orders

from ._gemini_market import GeminiMarket
from ._historical_market import HistoricalMarket
