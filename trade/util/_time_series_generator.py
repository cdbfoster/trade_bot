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
import itertools
import os.path

import numpy as np

class TimeSeriesGenerator:
    class Price(Enum):
        OPEN = "open"
        CLOSE = "close"
        HIGH = "high"
        LOW = "low"
        MEAN = "mean"

    def __init__(self, file_prefix):
        directory, file_prefix = os.path.split(file_prefix)
        if len(directory) == 0:
            directory = "."

        # Get all the files that start with file_prefix
        file_names = [file_name for file_name in os.listdir(directory) if file_name.startswith(file_prefix)]
        file_names.sort()

        class Trade:
            def __init__(self, time, price, volume):
                self.time = time
                self.price = price
                self.volume = volume

        # Read in the data from all files
        self.data = list(itertools.chain.from_iterable([[Trade(float(time), float(price), float(volume)) for time, price, volume in [line.strip().split() for line in open(directory + "/" + file_name)]] for file_name in file_names]))

        # TODO Detect/correct overlapping time

        # TODO Ensure chronological order of files

    def generate(self, file_prefix, interval_seconds, start_time=None, end_time=None, max_spacing_seconds=None, price=Price.CLOSE, volume=False):
        class Segment:
            def __init__(self, start, end, series, index):
                self.start = start
                self.end = end
                self.series = series
                self.index = index
                self.trades = []

                self.previous = None
                self.next = None

            def __find_previous(self):
                current_index = self.index
                while current_index > 0:
                    current_index -= 1
                    if len(self.series[current_index].trades) > 0:
                        return self.series[current_index]
                return None

            def open(self):
                if len(self.trades) == 0:
                    previous = self.__find_previous()
                    return previous.close() if previous is not None else 0

                return self.trades[0].price

            def close(self):
                if len(self.trades) == 0:
                    previous = self.__find_previous()
                    return previous.close() if previous is not None else 0

                return self.trades[-1].price

            def high(self):
                if len(self.trades) == 0:
                    previous = self.__find_previous()
                    return previous.high() if previous is not None else 0

                return max(trade.price for trade in self.trades)

            def low(self):
                if len(self.trades) == 0:
                    previous = self.__find_previous()
                    return previous.low() if previous is not None else 0

                return min(trade.price for trade in self.trades)

            def mean(self):
                if len(self.trades) == 0:
                    previous = self.__find_previous()
                    return previous.mean() if previous is not None else 0

                return np.mean(trade.price for trade in self.trades)

            def volume(self):
                return sum(trade.volume for trade in self.trades) if len(self.trades) > 0 else 0


        start_time = self.data[0].time if start_time is None else start_time
        end_time = self.data[-1].time if end_time is None else end_time

        segments = []
        segments.append(Segment(start_time, start_time + interval_seconds, segments, 0))
        trade_index = 0

        while trade_index < len(self.data):
            trade = self.data[trade_index]

            if trade.time < segments[-1].start:
                trade_index += 1
                continue
            elif trade.time > end_time:
                break

            if trade.time >= segments[-1].start and trade.time < segments[-1].end:
                segments[-1].trades.append(trade)
                trade_index += 1
            else:
                segments.append(Segment(segments[-1].end, segments[-1].end + interval_seconds, segments, len(segments)))

        if price is not None:
            prices_file = open("{}-{}s_{}-prices".format(file_prefix, interval_seconds, price.value), 'w')

        if volume:
            volume_file = open("{}-{}s_{}-volume".format(file_prefix, interval_seconds, price.value), 'w')

        for segment in segments:
            value = 0
            if price is TimeSeriesGenerator.Price.OPEN:
                value = segment.open()
            elif price is TimeSeriesGenerator.Price.CLOSE:
                value = segment.close()
            elif price is TimeSeriesGenerator.Price.HIGH:
                value = segment.high()
            elif price is TimeSeriesGenerator.Price.LOW:
                value = segment.low()
            elif price is TimeSeriesGenerator.Price.MEAN:
                value = segment.mean()

            # TODO Split the data into sections if more than max_spacing_seconds elapsed between trades

            if price is not None:
                prices_file.write("{:.2f}\n".format(value))

            if volume:
                volume_file.write("{}\n".format(segment.volume()))

        if price is not None:
            prices_file.close()

        if volume:
            volume_file.close()
