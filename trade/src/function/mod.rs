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

pub trait FunctionImpl<I, O>: Deref<Target = FunctionOutput<O>> where I: Copy, O: Clone {
    fn first(&mut self, input: I) -> O {
        self.next(input)
    }

    fn next(&mut self, input: I) -> O;

    fn get_function_output(&mut self) -> &mut FunctionOutput<O>;
}

pub trait Function<I, O>: FunctionImpl<I, O> where I: Copy, O: Clone {
    fn evaluate(&mut self, input: I) -> O {
        let result = if self.len() > 0 {
            self.next(input)
        } else {
            self.first(input)
        };

        self.get_function_output().push(result.clone());
        result
    }

    fn evaluate_sequence<'a>(&'a mut self, sequence: &[I]) -> &'a[O] {
        let current_index = self.len();

        for &x in sequence {
            self.evaluate(x);
        }

        &self[current_index..]
    }
}

impl<T, I, O> Function<I, O> for T where T: FunctionImpl<I, O>, I: Copy, O: Clone { }

pub type FunctionOutput<O> = Vec<O>;

pub use self::ema::{Ema, EmaDifference};

mod ema;
