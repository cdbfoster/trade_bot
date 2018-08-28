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

from trade.function.optimization import IntParameter, Optimizer

class MetropolisOptimizer(Optimizer):
    def __init__(self, iterations, std, verbose=False):
        self.iterations = iterations
        self.std = std
        self.verbose = verbose

    def optimize_parameters(self, function_class, acceptance_function):
        self.path = []

        parameters = function_class.optimizable_parameters()

        if self.verbose:
            print("Optimizing...")
            print("   0%")

        position, function = self.__starting_position(parameters, function_class)
        acceptance_score = acceptance_function(function)
        self.path.append((position, acceptance_score))

        best_position = position
        best_acceptance_score = acceptance_score

        for i in range(1, self.iterations):
            if self.verbose and i % (self.iterations // 20) == 0:
                print(" {:3.0f}%, best: ({}, {:.3f}), acceptance ratio: {:.4f}".format(
                    i // (self.iterations // 20) * 100 / 20,
                    best_position, best_acceptance_score,
                    self.acceptance_ratio,
                ))

            next_position, next_function = self.__next_position(parameters, function_class, position)
            next_acceptance_score = acceptance_function(next_function)

            if next_acceptance_score >= acceptance_score or np.random.uniform() > next_acceptance_score / max(acceptance_score, 0.00001):
                position = next_position
                acceptance_score = next_acceptance_score
                self.path.append((position, acceptance_score))

                if acceptance_score > best_acceptance_score:
                    best_position = position
                    best_acceptance_score = acceptance_score

            self.acceptance_ratio = len(self.path) / i if len(self.path) > 0 else 0.0

        if self.verbose and (self.iterations - 1) % (self.iterations // 20) != 0:
            print(" 100%, best: ({}, {:.3}), acceptance ratio: {:.4f}".format(best_position, best_acceptance_score, self.acceptance_ratio))

        return best_position

    def __starting_position(self, parameters, function_class):
        while True:
            position = [np.random.randint(p.minimum, p.maximum + 1) if isinstance(p, IntParameter) else np.random.uniform(p.minimum, p.maximum) for p in parameters]

            try:
                function = function_class(*position)
            except ValueError:
                pass
            else:
                return position, function

    def __next_position(self, parameters, function_class, position):
        next_position = position[:]

        while True:
            for i, p in enumerate(parameters):
                std = (p.maximum - p.minimum) * self.std

                while True:
                    sample = np.random.normal(position[i], std)

                    if isinstance(p, IntParameter):
                        sample = int(sample)

                    if sample <= p.maximum and sample >= p.minimum:
                        next_position[i] = sample
                        break

            try:
                function = function_class(*next_position)
            except ValueError:
                pass
            else:
                return next_position, function
