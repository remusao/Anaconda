/*
 * test.cc
 */
#include <vector>
#include <cassert>
#include "builtins.h"

int
main()
{
	// abs
	assert(Builtins::abs(-42) == 42);
	assert(Builtins::abs(0) == 0);
	assert(Builtins::abs(42) == 42);

	// all
	std::vector<bool> vec(42, true);
	assert(Builtins::all(vec));
	vec[40] = false;
	assert(Builtins::all(vec) == false);

	// any
	vec = std::vector<bool>(42, false);
	assert(Builtins::any(vec) == false);
	vec[40] = true;
	assert(Builtins::any(vec));

	// ascii
	assert(Builtins::ascii(42) == "42");
	assert(Builtins::ascii(42.42) == "42.42");
	assert(Builtins::ascii("42") == "42");

	// bin
	assert(Builtins::bin(42) == "0b101010");
	assert(Builtins::bin(-42) == "-0b101010");

	// bool
	assert(Builtins::toBool() == false);
	assert(Builtins::toBool(false) == false);
	assert(Builtins::toBool(true));
	assert(Builtins::toBool(42));
	assert(Builtins::toBool(0) == false);
	assert(Builtins::toBool(vec));
	vec.clear();
	assert(Builtins::toBool(vec) == false);

	// bytearray
	assert(Builtins::bytearray(42).size() == 42);
	assert(Builtins::bytearray().size() == 0);
	assert(Builtins::bytearray("toto").size() == 4);
	assert(Builtins::bytearray(std::string("toto")).size() == 4);
	assert(Builtins::bytearray(std::vector<unsigned char>(42, '*')).size() == 42);

	// bytes
	//auto r = Builtins::bytes();
	//r.push_back('*');
}

