/*
 * builtinsTest.cc
 *
 * <+DESC+>
 */
#include <iostream>
#include <vector>
#include <cassert>
#include "builtins.h"


int
main()
{
	// ABS
	assert(Builtins::abs(-42) == 42);
	assert(Builtins::abs(42) == 42);
	assert(Builtins::abs(0) == 0);
	assert(Builtins::abs(-0) == 0);

	// All
	std::vector<int> v1All = {1, 3, 42};
	std::vector<bool> v2All = {true, false, true};
	std::vector<bool> v3All = {false, false, false};
	std::vector<bool> v4All = {true, true, true};

	assert(Builtins::all(v1All) == true);
	assert(Builtins::all(v2All) == false);
	assert(Builtins::all(v3All) == false);
	assert(Builtins::all(v4All) == true);

	// Any
	assert(Builtins::any(v1All) == true);
	assert(Builtins::any(v2All) == true);
	assert(Builtins::any(v3All) == false);
	assert(Builtins::any(v4All) == true);


	// ascii
	assert(Builtins::ascii(42) == "42");
	assert(Builtins::ascii(42.0) == "42");
	assert(Builtins::ascii(42.1) == "42.1");
	assert(Builtins::ascii(-42.2) == "-42.2");
	assert(Builtins::ascii("foo") == "foo");

	// bin
	assert(Builtins::bin(42) == "0b101010");
	assert(Builtins::bin(-42) == "-0b101010");

	// toBool
	assert(Builtins::toBool() == false);
	assert(Builtins::toBool(42) == true);
	assert(Builtins::toBool(true) == true);
	assert(Builtins::toBool(false) == false);

	// byteArray
}

