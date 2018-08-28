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

import numpy as np

from trade.function.optimization import FixedParameter, IntParameter, Optimizer

class GridOptimizer(Optimizer):
    def __init__(self, divisions, verbose=False):
        self.divisions = divisions
        self.verbose = verbose

    def optimize_parameters(self, function_class, acceptance_function):
        parameters = function_class.optimizable_parameters()
        ranges = [np.linspace(p.minimum, p.maximum, num=self.divisions) if not isinstance(p, FixedParameter) else [p.value] for p in parameters]
        lengths = [len(range_) for range_ in ranges]

        for i, parameter in enumerate(parameters):
            if isinstance(parameter, IntParameter):
                ranges[i] = [int(x) for x in ranges[i]]
            elif isinstance(parameter, FixedParameter):
                continue

            ranges[i] = np.unique(ranges[i])

        combinations = np.prod(lengths)

        if self.verbose:
            self.__report_intervals = [int(x) for x in np.linspace(0, combinations, num=21)][::-1]
            self.__percent = 0
            print("Optimizing...")

        best_acceptance_score = None
        best_combination = None

        position = [0] * len(parameters)
        for iteration in range(combinations):
            if self.verbose:
                if iteration == self.__report_intervals[-1]:
                    print(" {:3}%".format(self.__percent), end="")
                    self.__report_intervals.pop()
                    self.__percent += 5

                    if best_combination:
                        print(", best: {}, score: {}".format(best_combination, best_acceptance_score))
                    else:
                        print()

            combination = [ranges[i][position[i]] for i in range(len(parameters))]

            try:
                function = function_class(*combination)
            except ValueError:
                pass
            else:
                acceptance_score = acceptance_function.acceptance_score(function)

                if best_acceptance_score is not None and acceptance_score > best_acceptance_score or best_acceptance_score is None:
                    best_acceptance_score = acceptance_score
                    best_combination = combination

            position[0] += 1
            for i in range(1, len(parameters)):
                if position[i - 1] >= lengths[i - 1]:
                    position[i - 1] = 0
                    position[i] += 1

        if self.verbose:
            print(" 100%, best: {}, score: {}".format(best_combination, best_acceptance_score))

        return best_combination
