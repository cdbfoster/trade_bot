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
from trade.market import _Market

class HistoricalMarket(_Market, HistoricalInputSource):
    def __init__(self, exchange_currency, base_currency, filename, start=None, position=None, reverse=False):
        _Market.__init__(self, exchange_currency, base_currency)
        HistoricalInputSource.__init__(self, filename, start, position, reverse)

    def buy(self, currency, other_amount):
        other = self.exchange_currency if currency == self.base_currency else self.base_currency
        rate = 1 / self[-1] if currency == self.exchange_currency else self[-1]

        amount = other_amount * rate
        if self.balance[other] < other_amount:
            return False

        self.balance[other] -= other_amount
        self.balance[currency] += amount
        return True

    def sell(self, currency, amount):
        other = self.exchange_currency if currency == self.base_currency else self.base_currency
        rate = self[-1] if currency == self.exchange_currency else 1 / self[-1]

        if self.balance[currency] < amount:
            return False

        other_amount = amount * rate
        self.balance[other] += other_amount
        self.balance[currency] -= amount
        return True
