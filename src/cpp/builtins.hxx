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
};
