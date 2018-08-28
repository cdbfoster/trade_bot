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

import sys

class OptimizableParameter:
    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

class FloatParameter(OptimizableParameter):
    def __init__(self, minimum=float("-inf"), maximum=float("inf")):
        self._minimum = float(minimum)
        self._maximum = float(maximum)

class IntParameter(OptimizableParameter):
    def __init__(self, minimum=(-sys.maxsize - 1), maximum=sys.maxsize):
        self._minimum = minimum
        self._maximum = maximum

class Optimizable:
    def optimizable_parameters():
        raise NotImplementedError

class Optimizer:
    def optimize_parameters(function_class, acceptance_function):
        raise NotImplementedError

from ._grid_optimizer import GridOptimizer
from ._metropolis_optimizer import MetropolisOptimizer
