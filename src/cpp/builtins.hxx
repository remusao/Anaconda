/*
 * builtins.cc
 */
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <bitset>

#include "builtins.h"

namespace Builtins
{
	/////////////////////
	/// Abs : cstdlib ///
	/////////////////////
	int abs(int n)
	{
		return ::abs(n);
	}

	long int abs(long int n)
	{
		return ::abs(n);
	}

	long long int abs(long long int n)
	{
		return ::abs(n);
	}


	///////////
	/// all ///
	///////////
	template <typename Iterable>
	bool all(const Iterable& it)
	{
		for (auto elt : it)
			if (!elt)
				return false;
		return true;
	}


	///////////
	/// any ///
	///////////
	template <typename Iterable>
	bool any(const Iterable& it)
	{
		for (auto elt : it)
			if (elt)
				return true;
		return false;
	}


	/////////////
	/// ascii ///
	/////////////
	template <typename Object>
	std::string ascii(const Object& obj)
	{
		std::stringstream ss(std::stringstream::in | std::stringstream::out);

		ss << obj;

		return ss.str();
	}

	template <>
	std::string ascii<std::string>(const std::string& obj)
	{
		return std::string(obj);
	}


	///////////
	/// bin ///
	///////////
	template <typename Object>
	std::string bin(const Object& obj)
	{
		return bin(obj.__index__());
	}

	namespace
	{
		template <typename IntegralType>
		std::string intToString(IntegralType i)
		{
			std::stringstream ss(std::stringstream::in | std::stringstream::out);

			if (i < 0)
			{
				ss << "-";
				i = -i;
			}

			auto result = std::bitset<sizeof (IntegralType) * 8>(i).to_string();
			ss << "0b" << result.substr(result.find('1'));

			return ss.str();
		}
	};

	template <>
	std::string bin<long long int>(const long long int& obj)
	{
		return intToString(obj);
	}

	template <>
	std::string bin<long int>(const long int& obj)
	{
		return intToString(obj);
	}

	template <>
	std::string bin<int>(const int& obj)
	{
		return intToString(obj);
	}


	////////////
	/// bool ///
	////////////
	namespace
	{
		template <typename Object>
		bool isTrue(const Object& obj) { return obj; }

		template <>
		bool isTrue<int>(const int& obj) { return obj; }

		template <>
		bool isTrue<long int>(const long int& obj) { return obj; }
		
		template <>
		bool isTrue<long long int>(const long long int& obj) { return obj; }
		
		template <>
		bool isTrue<float>(const float& obj) { return obj; }
		
		template <>
		bool isTrue<double>(const double& obj) { return obj; }
		
		template <>
		bool isTrue<bool>(const bool& obj) { return obj; }
	};

	template <>
	bool toBool()
	{
		return false;
	}

	template <typename T>
	bool toBool(const T& obj)
	{
		return isTrue(obj);
	}


	/////////////////
	/// bytearray ///
	/////////////////
	template <typename ... Arguments>
	std::vector<unsigned char> bytearray()
	{
		return std::vector<unsigned char>();
	}

	template <typename ... Arguments>
	std::vector<unsigned char> bytearray(int size)
	{
		return std::vector<unsigned char>(size, 0);
	}

	template <typename ... Arguments>
	std::vector<unsigned char> bytearray(const char s[])
	{
		auto tmp = std::string(s);
		return std::vector<unsigned char>(tmp.begin(), tmp.end());
	}

	template <typename ... Arguments>
	std::vector<unsigned char> bytearray(const std::string& s)
	{
		return std::vector<unsigned char>(s.begin(), s.end());
	}

	template <template <typename, typename> class Container, typename ... Arguments>
	std::vector<unsigned char> bytearray(const Container<unsigned char, std::allocator<unsigned char>>& c)
	{
		return std::vector<unsigned char>(c.begin(), c.end());
	}

	template <template <typename> class Container, typename ... Arguments>
	std::vector<unsigned char> bytearray(const Container<unsigned char>& c)
	{
		return std::vector<unsigned char>(c.begin(), c.end());
	}



	/////////////////
	/// bytearray ///
	/////////////////
	/*template <typename ... Arguments>
	const std::vector<unsigned char> bytes()
	{
		return std::vector<unsigned char>();
	}*/


	/////////////
	/// range ///
	/////////////

	namespace
	{
		template <bool Reverse>
		struct __RangeFunctor
		{
			private:
				long long int accu_;
				long long int stop_;
				long long int step_;
				coroutine __coroutine;

			public:
				__RangeFunctor() = delete;
				__RangeFunctor(const __RangeFunctor&) = default;
				__RangeFunctor& operator=(const __RangeFunctor&) = delete;

				__RangeFunctor(__RangeFunctor&&) = default;
				__RangeFunctor& operator=(__RangeFunctor&&) = default;
				__RangeFunctor(long long int start, long long int  stop, long long int step)
					: accu_(start), stop_(stop), step_(step)
				{
				}
				long long int operator()();
		};

		template <>
		long long int
		__RangeFunctor<false>::operator()()
		{
			reenter(this->__coroutine)
			{
				for (; accu_ < stop_; accu_ += step_)
					yield return accu_;
			}
			throw __EndOfGenerator();
		}

		template <>
		long long int
		__RangeFunctor<true>::operator()()
		{
			reenter(this->__coroutine)
			{
				for (; accu_ > stop_; accu_ += step_)
					yield return accu_;
			}
			throw __EndOfGenerator();
		}
	};

	__Generator<long long int> range(long long int start, long long int stop, long long int step)
	{
		// formula r[i] = start + step*i where i >= 0 and r[i] < stop.
		assert(step != 0);

		if (step < 0)
		{
			assert(stop < start);
			return __Generator<long long int>(__RangeFunctor<true>(start, stop, step));
		}
		else
		{
			assert(stop > start);
			return __Generator<long long int>(__RangeFunctor<false>(start, stop, step));
		}
	}

	__Generator<long long int> range(long long int stop)
	{
		return range(0, stop, 1);
	}


	/////////////
	/// print ///
	/////////////

	template <typename Arg, typename ...Arguments>
	void print(const Arg& first, const Arguments... args)
	{
		std::cout << first << ' ';
		print(args...);
	}

	template <>
	void print()
	{
		std::cout << std::endl;
	}
};
