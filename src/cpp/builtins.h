#pragma once
#ifndef BUILTINS_H
# define BUILTINS_H

# include <string>
# include <vector>
# include "coroutine.h"
# include "yield.h"
# include "generator.h"


namespace Builtins
{
	/// @func abs(x)  -  stdlib
	/// @brief Return the absolute value of a number.
	int abs(int n);
	long int abs(long int n);
	long long int abs(long long int n);


	/// @func all(iterable)
	/// @brief Return True if all elements of the iterable are true (or if the
	/// iterable is empty).
	template <typename Iterable>
	bool all(const Iterable& it);


	/// @func any(iterable)
	/// @brief Return True if any element of the iterable is true. If the iterable
	/// is empty, return False.
	template <typename Iterable>
	bool any(const Iterable& it);


	/// @func ascii(object)
	/// @brief As repr(), return a string containing a printable representation
	/// of an object, but escape the non-ASCII characters in the string returned
	/// by repr() using \x, \u or \U escapes. This generates a string similar to
	/// that returned by repr() in Python 2.
	template <typename Object>
	std::string ascii(const Object& obj);


	/// @func bin(x)
	/// @brief Convert an integer number to a binary string. The result is a
	/// valid Python expression. If x is not a Python int object, it has to define
	/// an __index__() method that returns an integer.
	template <typename Object>
	std::string bin(const Object& obj);


	/// @func  bool([x])
	/// @brief Convert a value to a Boolean, using the standard truth testing
	/// procedure. If x is false or omitted, this returns False; otherwise it
	/// returns True.
	template <typename ... Arguments>
	bool toBool(const Arguments&... obj);


	/// @func bytearray([source[, encoding[, errors]]])
	/// @brief Return a new array of bytes. The bytearray type is a mutable
	/// sequence of integers in the range 0 <= x < 256. It has most of the usual
	/// methods of mutable sequences, described in Mutable Sequence Types, as well
	/// as most methods that the bytes type has, see Bytes and Bytearray
	/// Operations.
	/// The optional source parameter can be used to initialize the array in a few
	/// different ways:
	///
	/// * If it is a string, you must also give the encoding (and optionally,
	///  errors) parameters; bytearray() then converts the string to bytes
	///  using str.encode().
	///	* If it is an integer, the array will have that size and will be
	///  initialized with null bytes.
	/// * If it is an object conforming to the buffer interface, a
	///  read-only buffer of the object will be used to initialize the
	///  bytes array.
	/// * If it is an iterable, it must be an iterable of integers
	///  in the range 0 <= x < 256, which are used as the initial
	///  contents of the array.
	///
	///	Without an argument, an array of size 0 is created.
	template <typename ... Arguments>
	std::vector<unsigned char> bytearray(const Arguments&... args);


	/// @func bytes([source[, encoding[, errors]]])
	/// @brief Return a new “bytes” object, which is an immutable sequence of
	/// integers in the range 0 <= x < 256. bytes is an immutable version of
	/// bytearray – it has the same non-mutating methods and the same indexing and
	/// slicing behavior.
	///
	/// Accordingly, constructor arguments are interpreted as for bytearray().
	//template <typename ... Arguments>
	//const std::vector<unsigned char> bytes(const Arguments&... args);
	// TODO : Implements a const vector

	/// @func range(stop)
	/// @func range(start, stop[, step])
	/// @brief The arguments to the range constructor must be integers (either
	/// built-in int or any object that implements the __index__ special method).
	/// If the step argument is omitted, it defaults to 1. If the start argument
	/// is omitted, it defaults to 0. If step is zero, ValueError is raised.
	///
	/// For a positive step, the contents of a range r are determined by the
	/// formula r[i] = start + step*i where i >= 0 and r[i] < stop.
	///
	/// For a negative step, the contents of the range are still determined by the
	/// formula r[i] = start + step*i, but the constraints are i >= 0 and r[i] >
	/// stop.
	///
	/// A range object will be empty if r[0] does not meant the value constraint.
	/// Ranges do support negative indices, but these are interpreted as indexing
	/// from the end of the sequence determined by the positive indices.
	///
	/// Ranges containing absolute values larger than sys.maxsize are permitted
	/// but some features (such as len()) may raise OverflowError.
	__Generator<long long int> range(long long int stop);
	__Generator<long long int> range(long long int start, long long int stop, long long int step = 1);
/*
		__import__()
		callable()
		chr()
		classmethod()
		compile()
		complex()
		delattr()
		dict()
		dir()
		divmod()
		enumerate()
		eval()
		exec()
		filter()
		float()
		format()
		frozenset()
		getattr()
		globals()
		hasattr()
		hash()
		help()
		hex()
		id()
		input()
		int()
		isinstance()
		issubclass()
		iter()
		len()
		list()
		locals()
		map()
		max()
		memoryview()
		min()
		next()
		object()
		oct()
		open()
		ord()
		pow()
		print()
		property()
		repr()
		reversed()
		round()
		set()
		setattr()
		slice()
		sorted()
		staticmethod()
		str()
		sum()
		super()
		tuple()
		type()
		vars()
		zip()
		*/
};

// Implemantation
# include "builtins.hxx"

#endif /* ndef BUILTINS_H */
