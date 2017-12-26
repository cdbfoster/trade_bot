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

from trade.function import _Function
from trade.market import _Market, OrderSide, OrderType
from trade.util import WebSocketClient

class GeminiMarket(_Function, _Market):
    class Symbol(Enum):
        BTCUSD = "btcusd"
        ETHUSD = "ethusd"
        ETHBTC = "ethbtc"

    def __init__(self, symbol, public_key=None, private_key=None, reset_timeout=10, sandbox=False):
        pass

class PublicListener(WebSocketClient):
    def __init__(self, symbol, reset_timeout, sandbox):
        self.url = "wss://api.{}gemini.com/v1/marketdata/{}?heartbeat=true".format("sandbox." if sandbox == True else "", symbol.name)
        WebSocketClient.__init__(self, self.url, reset_timeout)

        self.trades_file = open("gemini_{}_trades".format(symbol.value), 'a')

    def close(self):
        WebSocketClient.close(self)
        self.trades_file.close()

    def on_open(self, ws):
        pass

    def on_message(self, ws, message):
        data = json.loads(message)
        if data["type"] == "update":
            for event in data["events"]:
                if event["type"] == "trade":
                    timestamp = data["timestampms"] / 1000
                    self.trades_file.write("{:.3f} {:.2f} {}\n".format(timestamp, float(event["price"]), float(event["amount"])))

    def on_close(self, ws):
        pass
