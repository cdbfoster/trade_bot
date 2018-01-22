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

def up_price(current_price, trade_loss, transaction_fee):
    """ If we buy at current_price, we gain as if we had bought at the returned price.
        Conversly, we can sell at the returned price to gain as if we had sold at current_price. """
    return current_price * (1 + trade_loss) / (1 - transaction_fee)

def down_price(current_price, trade_loss, transaction_fee):
    """ If we sell at current_price, we gain as if we had sold at the returned price.
        Conversly, we can buy at the returned price to gain as if we had bought at current_price. """
    return current_price * (1 - transaction_fee) / (1 + trade_loss)

def return_price(current_price, trade_loss, transaction_fee, desired_return, speculative=False):
    """ If we bought (or buy, if speculative is True) at current_price, we'd have to sell at the returned price to make (100 * desired_return)% profit. """
    buy_price = up_price(current_price, trade_loss, transaction_fee) if speculative else current_price
    sell_price = up_price(buy_price * (1 + desired_return), trade_loss, transaction_fee)
    return sell_price

def return_value(current_price, trade_loss, transaction_fee, bought_price):
    """ If we were to sell at current_price, given that we bought at bought_price, we'd gain the returned value. """
    return down_price(current_price, trade_loss, transaction_fee) / bought_price - 1
