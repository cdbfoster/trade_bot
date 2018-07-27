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

def buy_down_price(current_price, trade_loss, transaction_fee):
    """ If we buy at the returned price, we gain as if we had bought at current_price with no loss or fees. """
    return current_price / (1 + trade_loss) / (1 + transaction_fee)

def buy_up_price(current_price, trade_loss, transaction_fee):
    """ If we buy at current_price, we gain as if we had bought at the returned price with no loss or fees. """
    return current_price * (1 + trade_loss) * (1 + transaction_fee)

def return_down_price(current_price, trade_loss, transaction_fee, desired_return):
    """ If we sell at current_price, we'd have to have bought at the returned price to make (100 * desired_return)% profit. """
    sell_price = sell_down_price(current_price, trade_loss, transaction_fee)
    buy_price = buy_down_price(sell_price / (1 + desired_return), trade_loss, transaction_fee)
    return buy_price

def return_up_price(current_price, trade_loss, transaction_fee, desired_return):
    """ If we buy at current_price, we'd have to sell at the returned price to make (100 * desired_return)% profit. """
    buy_price = buy_up_price(current_price, trade_loss, transaction_fee)
    sell_price = sell_up_price(buy_price * (1 + desired_return), trade_loss, transaction_fee)
    return sell_price

def return_value(current_price, bought_price, trade_loss, transaction_fee):
    """ If we sell at current_price having bought at bought_price, we'd make (the returned value * 100)% profit. """
    return sell_down_price(current_price, trade_loss, transaction_fee) / bought_price - 1

def sell_down_price(current_price, trade_loss, transaction_fee):
    """ If we sell at current_price, we gain as if we had sold at the returned price with no loss or fees. """
    return current_price * (1 - trade_loss) * (1 - transaction_fee)

def sell_up_price(current_price, trade_loss, transaction_fee):
    """ If we sell at the returned price, we gain as if we had sold at current_price with no loss or fees. """
    return current_price / (1 - trade_loss) / (1 - transaction_fee)
