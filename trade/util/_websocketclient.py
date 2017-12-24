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

import datetime
from functools import partial
import ssl
import sys
import threading
import time
import websocket

class WebSocketClient:
    def __init__(self, url, reset_timeout):
        self.reset_timeout = reset_timeout
        self.closed = False

        self.url = url

        self.__ws_reset_event = threading.Event()
        self.__ws_reset_timer = None

        self.__input_thread = threading.Thread(target=self.__run_input_thread)
        self.__input_thread.daemon = True
        self.__input_thread.start()

        self.__ws_reset_event.set()

    def close(self):
        self.closed = True
        self.__ws.close()

    def on_open(self, ws):
        pass

    def on_message(self, ws, message):
        pass

    def on_close(self, ws):
        pass

    def on_error(self, ws, error):
        pass

    def __run_input_thread(self):
        while self.__ws_reset_event.wait():
            self.__ws_reset_event.clear()

            if not self.closed:
                self.__ws = websocket.WebSocketApp(self.url, on_open=self.__on_open, on_message=self.__on_message, on_close=self.__on_close, on_error=self.__on_error)

                if self.__ws_reset_timer is not None:
                    self.__ws_reset_timer.cancel()
                self.__ws_reset_timer = threading.Timer(self.reset_timeout, self.__ws.close)

                run_forever = partial(self.__ws.run_forever, sslopt={"cert_reqs": ssl.CERT_NONE})
                wst = threading.Thread(target=run_forever)
                wst.daemon = True
                wst.start()

                self.__ws_reset_timer.start()
            else:
                break

    def __on_open(self, ws):
        self.on_open(ws)

    def __on_message(self, ws, message):
        self.__ws_reset_timeout()
        self.on_message(ws, message)

    def __on_close(self, ws):
        self.on_close(ws)
        time.sleep(1)
        self.__ws_reset_event.set()

    def __on_error(self, ws, error):
        sys.stderr.write("{}: {}\n".format(datetime.datetime.now(), error))
        self.on_error(ws, error)

    def __ws_reset_timeout(self):
        if self.reset_timeout is not None:
            self.__ws_reset_timer.cancel()
            self.__ws_reset_timer = threading.Timer(self.reset_timeout, self.__ws.close)
            self.__ws_reset_timer.start()
