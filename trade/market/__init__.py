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

class _Market:
    def __init__(self, exchange_currency, base_currency):
        self.exchange_currency = exchange_currency
        self.base_currency = base_currency

        self.currencies = (exchange_currency, base_currency)

        self.balance = {
            exchange_currency: 0.0,
            base_currency: 0.0,
        }

    def buy(self, currency, other_amount):
        pass

    def sell(self, currency, amount):
        pass

from ._historical_market import HistoricalMarket
