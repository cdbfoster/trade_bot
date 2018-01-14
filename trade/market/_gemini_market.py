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

from enum import Enum
import json
import threading

from trade.function import Function
from trade.market import _Market, OrderSide, OrderType
from trade.util import WebSocketClient

class GeminiMarket(Function, _Market):
    class Symbol(Enum):
        BTCUSD = "btcusd"
        ETHUSD = "ethusd"
        ETHBTC = "ethbtc"

    def __init__(self, symbol, public_key=None, private_key=None, reset_timeout=10, sandbox=False, record_trades=True):
        self.__symbol = symbol
        self.__public_key = public_key
        self.__private_key = private_key

        self.__prices = []

        self.__public_listener = PublicListener(self.__symbol, reset_timeout, sandbox, record_trades)

    def __getitem__(self, value):
        return self.__prices[value]

    def __len__(self):
        return len(self.__prices)

    def update(self, steps=1):
        if steps != 1:
            raise ValueError("Gemini market cannot update more than one step.")

        last_trade_price = self.__public_listener.last_trade_price
        if last_trade_price is not None:
            self.__prices.append(last_trade_price)

    def place_order(self, order_side, order_type, amount, cancel_existing=True):
        pass

    def cancel_active_orders(self):
        pass

    def get_last_price(self):
        return self[-1]

    def get_orders(self, side):
        with self.__public_listener.orders_lock:
            if side == OrderSide.BUY:
                return sorted(self.__public_listener.orders_buy.items(), reverse=True)
            else:
                return sorted(self.__public_listener.orders_sell.items())

class PublicListener(WebSocketClient):
    def __init__(self, symbol, reset_timeout, sandbox, record_trades):
        self.url = "wss://api.{}gemini.com/v1/marketdata/{}?heartbeat=true".format("sandbox." if sandbox == True else "", symbol.name)
        WebSocketClient.__init__(self, self.url, reset_timeout)

        self.trades_file = open("gemini_{}_trades".format(symbol.value), 'a') if record_trades else None
        self.last_trade_price = None

        self.orders_lock = threading.Lock()
        self.orders_buy = {}
        self.orders_sell = {}

    def close(self):
        WebSocketClient.close(self)
        if self.trades_file is not None:
            self.trades_file.close()

    def on_open(self, ws):
        self.orders_buy = {}
        self.orders_sell = {}

    def on_message(self, ws, message):
        data = json.loads(message)
        if data["type"] == "update":
            for event in data["events"]:
                if event["type"] == "trade":
                    timestamp = data["timestampms"] / 1000
                    price = float(event["price"])
                    amount = float(event["amount"])

                    if self.trades_file is not None:
                        self.trades_file.write("{:.3f} {:.2f} {}\n".format(timestamp, price, amount))
                        self.trades_file.flush()

                    self.last_trade_price = price
                elif event["type"] == "change":
                    with self.orders_lock:
                        side = self.orders_sell if event["side"] == "ask" else self.orders_buy

                        if event["remaining"] == "0":
                            del side[float(event["price"])]
                        else:
                            side[float(event["price"])] = float(event["remaining"])

    def on_close(self, ws):
        pass
