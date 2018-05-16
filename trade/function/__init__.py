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

class Function:
    def __init__(self):
        self.inputs = FunctionInputs()
        self._values = []

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
        self._next()

    def _next(self):
        raise StopIteration

    def _update(self):
        self.inputs.update()
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

    def save(self, filename, mode='w', save_inputs=False):
        f = open(filename, mode)

        if save_inputs:
            f.write("# ")
            for input_ in self.inputs:
                f.write("{} ".format(input_.name))
            f.write("value\n")

        for i, x in enumerate(self):
            if save_inputs:
                for input_ in self.inputs:
                    f.write("{} ".format(input_[i - len(self)]))
            f.write("{}\n".format(x))
        f.close()

    def __iter__(self):
        return Function.__Iter(self)

    class __Iter:
        def __init__(self, function):
            self.function = function
            self.position = 0

            self.function._update()

        def __next__(self):
            if self.position < len(self.function):
                self.position += 1
                return self.function[self.position - 1]
            raise StopIteration

class FunctionInputs(set):
    def __init__(self):
        set.__init__(self)
        self.__synced = False

    def sync_to_min_length(self, sync_offset=-1, resync=False):
        if self.__synced and not resync:
            return
        self.__synced = True

        lengths = [len(core) for core in [i._FunctionInput__core for i in self if hasattr(i._FunctionInput__core, "__len__")]]
        min_length = min(lengths) if len(lengths) > 0 else 0

        for i in self:
            offset = len(i) - min_length - i.consumed + sync_offset
            if offset > 0:
                i.consume(offset)

    def sync_to_input_index(self, input_, index, sync_offset=-1, resync=False):
        if self.__synced and not resync:
            return
        self.__synced = True

        if input_ is not None:
            input_length = len(input_)
        else:
            lengths = [len(core) for core in [i.__core for i in self if hasattr(i.__core, "__len__")]]
            input_length = max(lengths) if len(lengths) > 0 else 0

        for i in self:
            offset = len(i) - input_length + index - i.consumed + sync_offset
            if offset > 0:
                i.consume(offset)

    def update(self):
        for i in self:
            i.update()

class FunctionInput:
    def __init__(self):
        self.name = None
        self.__core = None
        self.__consumed = 0
        self.__function = None

    def consume(self, count=1):
        if not isinstance(count, int) or count <= 0:
            raise ValueError("must consume a positive integer greater than zero")

        if self.__consumed + count > len(self):
            raise ValueError("consumed past the end of the function input")

        if count == 1:
            self.__consumed += 1
            return self[self.__consumed - 1]
        else:
            values = slice(self.__consumed, self.__consumed + count)
            self.__consumed += count
            return self[values]

    @property
    def consumed(self):
        return self.__consumed

    @property
    def max(self):
        if hasattr(self, "_FunctionInput__max"):
            return self.__max
        elif isinstance(self.__core, int) or isinstance(self.__core, float):
            return self.__core
        else:
            raise AttributeError("'FunctionInput' object has no attribute 'max'")

    def update(self):
        if isinstance(self.__core, Function):
            self.__core._update()

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if isinstance(instance, Function):
            instance.inputs.add(self)
            self.__function = instance

        if isinstance(value, tuple) and len(value) >= 2 and isinstance(value[0], Function):
            self.__core = value[0]
            self.__max = value[1]
        else:
            self.__core = value
        self.__consumed = 0

    def __len__(self):
        if hasattr(self.__core, "__len__"):
            return len(self.__core)
        elif self.__function is not None:
            lengths = [len(core) for core in [i.__core for i in self.__function.inputs if hasattr(i.__core, "__len__")]]
            return min(lengths) if len(lengths) > 0 else len(self.__function) + 1
        else:
            return 0

    def __getitem__(self, index):
        if hasattr(self.__core, "__getitem__"):
            return self.__core[index]
        else:
            length = len(self)
            if isinstance(index, int):
                if index >= length or index < -length:
                    raise ValueError("function input index out of range")
                else:
                    return self.__core
            elif isinstance(index, slice):
                if index.start is not None and not isinstance(index.start, int):
                    raise TypeError("slice indices must be integers or None")
                if index.stop is not None and not isinstance(index.stop, int):
                    raise TypeError("slice indices must be integers or None")

                start = min(len(self.__function) + index.start + (length if index.start < 0 else 0), length)
                stop = min(len(self.__function) + index.stop + (length if index.stop < 0 else 0), length)
                step = index.step if index.step is not None else 1
                return [self.__core] * len(range(start, stop, step))
            else:
                raise TypeError("function input indices must be integers or slices")

    def __get_offset(self):
        lengths = [len(core) for core in [i.__core for i in self.__function.inputs if hasattr(i.__core, "__len__")]]
        min_length = min(lengths) if len(lengths) > 0 else 0
        return len(self) - min_length

from ._arithmetic import Add, Divide, Multiply, Subtract
from ._aroon import AroonUp, AroonDown, AroonOscillator
from ._atr import Atr
from ._change_period import ChangePeriod, change_period
from ._ehlers_way_bandpass import EhlersWayBandpass, ehlers_way_bandpass
from ._ema import Ema, ema
from ._historical_input import HistoricalInput, historical_input
from ._macd import Macd, MacdHistogram, macd, macd_histogram
from ._pooling import Close, High, Low, Open
from ._skip import Skip
from ._chandelier_exit import ChandelierExitLong, ChandelierExitShort # Needs Atr, High, Low, Skip
from ._slope import Slope, slope
from ._rsi import Rsi, rsi # Needs Slope
from ._standard_deviation import StandardDeviation, standard_deviation
from ._dominant_band import DominantBand, dominant_band # Needs EhlersWayBandpass, StandardDeviation
from ._z_score import ZScore, z_score
