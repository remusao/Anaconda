/*
 * testGenerator.cc
 *
 * <+DESC+>
 */
#include <memory>
#include <iostream>
#include "generator.h"
#include "coroutine.h"
#include "yield.h"


Generator<long int>
my_range(long int start, long int end, long int step)
{
	coroutine c;
	return Generator<long int>([=, &c](bool& over) mutable -> long int
	{
		over = false;
		reenter(c)
		{
			for (; start < end; ++start)
				yield;// return start;
			over = true;
			yield;
		}
	});
}


int
main()
{
	for (auto x : my_range(0, 10, 1))
		std::cout << x << std::endl;

	return 0;
}
