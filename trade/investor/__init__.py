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

class Investor:
    def __init__(self, market, exchange_amount=None, base_amount=None):
        self.market = market

        if exchange_amount is not None:
            self.market.balance[self.market.exchange_currency] = exchange_amount

        if base_amount is not None:
            self.market.balance[self.market.base_currency] = base_amount

    def tick(self):
        pass

from ._singleindicator_investor import SingleIndicatorInvestor
