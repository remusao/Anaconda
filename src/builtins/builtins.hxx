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
		bool isTrue(const Object& obj) { return obj.size(); }

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

	template <typename ... Arguments>
	bool toBool(const Arguments&... args)
	{
		static_assert((sizeof...(args)) == 0, "Args should be empty.");
		return false;
	}

	template <typename T, typename ... Arguments>
	bool toBool(const T& obj, Arguments... args)
	{
		static_assert((sizeof...(args)) == 0,
			"Builtin bool can't take more than 1 argument.");

		return isTrue(obj);
	}
};
