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
	return Generator<long int>([=]() mutable -> long int
	{
		reenter(c)
		{
			for (; start < end; start += step)
				yield return start;
		}
		throw EndOfGenerator();
	});
}

Generator<long int>
my_range2()


int
main()
{
	for (auto x : my_range(0, 1000000000, 42))
		std::cout << x;
	std::cout << std::endl;

	return 0;
}
