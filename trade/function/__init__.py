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

class _Function:
    def __init__(self):
        self._values = []
        self._exhaust_input()

    def __len__(self):
        return len(self._values)

    def __getitem__(self, index):
        if isinstance(index, int):
            self.__ensure_index(index)

            if index >= len(self) or index < -len(self):
                raise ValueError("function index out of range")

            if index < 0:
                index += len(self)

            return self._values[index]
        elif isinstance(index, slice):
            if index.start is not None and not isinstance(index.start, int):
                raise TypeError("slice indices must be integers or None")
            if index.stop is not None and not isinstance(index.stop, int):
                raise TypeError("slice indices must be integers or None")

            if index.stop is None or index.stop < 0:
                self.__ensure_index(-1)
            else:
                self.__ensure_index(index.stop)

            return self._values[index]
        else:
            raise TypeError("function indices must be integers or slices")

    def _first(self):
        pass

    def _next(self):
        pass

    def _exhaust_input(self):
        self.__ensure_index(-1)

    def __ensure_index(self, index):
        while len(self) <= index if index > 0 else True:
            try:
                if len(self._values) == 0:
                    self._first()
                else:
                    self._next()
            except StopIteration:
                break

    def save(self, filename, mode='w', save_input=False):
        f = open(filename, mode)
        for i, x in enumerate(self):
            if save_input and 'input' in dir(self):
                f.write("{} ".format(self.input[i - len(self)]))
            f.write("{}\n".format(x))
        f.close()

    def __iter__(self):
        return _Function.__Iter(self)

    class __Iter:
        def __init__(self, function):
            self.function = function
            self.position = 0

            self.function._exhaust_input()

        def __next__(self):
            if self.position < len(self.function):
                self.position += 1
                return self.function[self.position - 1]
            raise StopIteration

from ._aroon_functions import AroonUpFunction, AroonDownFunction, AroonOscillatorFunction
from ._difference_function import DifferenceFunction
from ._ema_function import EmaFunction
from ._historicalinput_function import HistoricalInputFunction
from ._macd_function import MacdFunction
from ._macdhistogram_function import MacdHistogramFunction
from ._movingsum_function import MovingSumFunction
from ._rsi_function import RsiFunction
from ._rsicenterline_function import RsiCenterlineFunction
