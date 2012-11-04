#include "coroutine.h"
#include "yield.h"
#include "generator.h"
#include <vector>
#include <iostream>




/*
Generator(Name, int,
	// Prologue
	size_t i;
,
	// Body
	yield return 42;
	yield return 1;
	for (i = 0; i < 42; ++i)
		yield return i;
)
		reenter(c)
        {
			yield return 42;
			for (; begin != end; ++begin)
				yield return *begin;
        }

        throw EndOfGenerator();
    });
}
*/


template <typename T1, typename T2, typename T3>
auto myRange(T1 start, T2 end, T3 step) -> __Generator<long int>
{
		struct myRangeFunctor
		{
			// Attributes
			coroutine c;
			T1 start;
			T2 end;
			T3 step;
			decltype(start) i;

			// Constructors

			myRangeFunctor(T1 start_, T2 end_, T3 step_)
			{
				start = start_;
				end = end_;
				step = step_;
			}

			// Delete other constructors

			long int operator()()
			{
				reenter(this->c)
				{
					for (; this->start < this->end; this->start += this->step)
						yield return this->start;
				}

				throw __EndOfGenerator();
			}
		};

    return __Generator<long int>(myRangeFunctor(start, end, step));
}

int main()
{
    for (auto x : myRange(0, 1000000000, 42))
		std::cout << x << "\n";

	std::cout << std::endl;

}
