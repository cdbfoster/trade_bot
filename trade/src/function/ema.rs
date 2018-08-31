// This file is part of trade_bot.
//
// trade_bot is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// trade_bot is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with trade_bot.  If not, see <http://www.gnu.org/licenses/>.

use std::ops::Deref;

use function::{Function, FunctionImpl, FunctionOutput};

pub struct Ema {
    period: u32,

    last_value: f32,
    weight: f32,

    output: FunctionOutput<f32>,
}

impl Ema {
    pub fn new(period: u32) -> Self {
        Self {
            period: period,
            last_value: 0.0,
            weight: 2.0 / (period as f32 + 1.0),
            output: FunctionOutput::new(),
        }
    }

    pub fn get_period(&self) -> u32 {
        self.period
    }
}

impl FunctionImpl<f32, f32> for Ema {
    fn first(&mut self, input: f32) -> f32 {
        self.last_value = input;
        input
    }

    fn next(&mut self, input: f32) -> f32 {
        self.last_value = input * self.weight + self.last_value * (1.0 - self.weight);
        self.last_value
    }

    fn get_function_output(&mut self) -> &mut FunctionOutput<f32> {
        &mut self.output
    }
}

impl Deref for Ema {
    type Target = FunctionOutput<f32>;

    fn deref(&self) -> &FunctionOutput<f32> {
        &self.output
    }
}

pub struct EmaDifference {
    pub period_a: u32,
    pub period_b: u32,

    ema_a: Ema,
    ema_b: Ema,

    output: FunctionOutput<f32>,
}

impl EmaDifference {
    pub fn new(period_a: u32, period_b: u32) -> Self {
        Self {
            period_a: period_a,
            period_b: period_b,
            ema_a: Ema::new(period_a),
            ema_b: Ema::new(period_b),
            output: FunctionOutput::new(),
        }
    }

    pub fn get_period_a(&self) -> u32 {
        self.period_a
    }

    pub fn get_period_b(&self) -> u32 {
        self.period_b
    }
}

impl FunctionImpl<f32, f32> for EmaDifference {
    fn next(&mut self, input: f32) -> f32 {
        self.ema_a.evaluate(input) - self.ema_b.evaluate(input)
    }

    fn get_function_output(&mut self) -> &mut FunctionOutput<f32> {
        &mut self.output
    }
}

impl Deref for EmaDifference {
    type Target = FunctionOutput<f32>;

    fn deref(&self) -> &FunctionOutput<f32> {
        &self.output
    }
}
